#!/usr/bin/env python3
"""
Zero-Dependency Python Stdio MCP Server for CEA Digital Actor #1:
Skip Trace & Property / LLC Owner Phone Finder + OFAC KYB.

Implements JSON-RPC 2.0 (initialize, tools/list, tools/call, ping) over stdio.
Routes tool calls to https://ceadigital.io/v1/tools/skip-trace-owner-phone-finder
(or https://ceadigital.io/v1/tools/free-preview in zero-config sandbox mode).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

DIRECT_ENDPOINT = "https://ceadigital.io/v1/tools/skip-trace-owner-phone-finder"
FREE_PREVIEW_ENDPOINT = "https://ceadigital.io/v1/tools/free-preview"
APIFY_ENDPOINT = "https://api.apify.com/v2/acts/cea_digital~skip-trace-owner-phone-finder/run-sync-get-dataset-items"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "skip_trace_owner_phone_finder",
        "description": (
            "Pierce anonymous real estate LLCs or property owner names to identify the human "
            "managing member/registered agent, resolve verified wireless mobile phone numbers "
            "and deliverable emails, geocode the parcel via U.S. Census TigerWeb, and screen "
            "against U.S. Treasury OFAC SDN and GLEIF LEI KYB registries. "
            "Use when an user or agent needs owner contact phones/emails for off-market real estate, "
            "commercial properties, tax-delinquent parcels, or B2B KYB diligence. "
            "Supports zero-key 1-row live preview or full batch execution with CEA_API_KEY."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "companyOrOwnerNames": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 2, "maxLength": 200},
                    "minItems": 1,
                    "maxItems": 25,
                    "description": (
                        "Array of LLC entity names or individual property owner names to pierce and skip-trace "
                        "(1 to 25 items per call). Example: ['PALMETTO INDUSTRIAL HOLDINGS LLC']."
                    ),
                    "default": ["PALMETTO INDUSTRIAL HOLDINGS LLC"],
                },
                "addresses": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 5, "maxLength": 300},
                    "minItems": 1,
                    "maxItems": 25,
                    "description": (
                        "Corresponding street addresses with city, state, and 5-digit ZIP code "
                        "(1 to 25 items). Example: ['1201 Main St Ste 1980, Columbia, SC 29201']."
                    ),
                    "default": ["1201 Main St Ste 1980, Columbia, SC 29201"],
                },
                "reportType": {
                    "type": "string",
                    "enum": [
                        "skip_trace_only",
                        "pierce_llc_and_skip_trace",
                        "full_kyb_guarantor_diligence",
                    ],
                    "default": "pierce_llc_and_skip_trace",
                    "description": (
                        "Enrichment tier: 'skip_trace_only' returns wireless/landline phones and emails; "
                        "'pierce_llc_and_skip_trace' adds corporate LLC officer/registered agent piercing "
                        "and U.S. Census geocoding; 'full_kyb_guarantor_diligence' adds GLEIF LEI and "
                        "U.S. Treasury OFAC SDN sanctions screening."
                    ),
                },
                "includeLiens": {
                    "type": "boolean",
                    "default": True,
                    "description": "When true, includes involuntary lien, tax delinquency, and pre-foreclosure flags.",
                },
            },
            "required": ["companyOrOwnerNames", "addresses"],
        },
        "annotations": {
            "title": "Skip Trace & LLC Owner Phone Finder",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    }
]


def _call_upstream(args: dict[str, Any]) -> dict[str, Any] | list[Any]:
    names = args.get("companyOrOwnerNames") or ["PALMETTO INDUSTRIAL HOLDINGS LLC"]
    addresses = args.get("addresses") or ["1201 Main St Ste 1980, Columbia, SC 29201"]
    report_type = args.get("reportType") or "pierce_llc_and_skip_trace"
    include_liens = bool(args.get("includeLiens", True))

    payload = {
        "companyOrOwnerNames": names,
        "addresses": addresses,
        "reportType": report_type,
        "includeLiens": include_liens,
    }

    cea_key = os.environ.get("CEA_API_KEY", "").strip()
    apify_token = os.environ.get("APIFY_TOKEN", "").strip()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ceadigital-skip-trace-mcp/1.2.0",
    }

    if cea_key:
        url = DIRECT_ENDPOINT
        headers["Authorization"] = f"Bearer {cea_key}"
        body = json.dumps(payload).encode("utf-8")
    elif apify_token:
        url = f"{APIFY_ENDPOINT}?token={apify_token}"
        body = json.dumps(payload).encode("utf-8")
    else:
        url = FREE_PREVIEW_ENDPOINT
        preview_payload = {
            "tool": "skip-trace-owner-phone-finder",
            "input": payload,
        }
        body = json.dumps(preview_payload).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as err:
        err_body = err.read().decode("utf-8", errors="replace")
        return {
            "status": "http_error",
            "code": err.code,
            "message": err_body[:500],
            "upgrade_url": "https://ceadigital.io/tools",
            "apify_actor_url": "https://apify.com/cea_digital/skip-trace-owner-phone-finder",
        }
    except Exception as exc:
        return {
            "status": "preview_fallback",
            "note": f"Upstream network unreachable in sandbox ({exc}); returning deterministic schema sample.",
            "sample": {
                "inputEntity": names[0],
                "inputAddress": addresses[0],
                "piercedManagingMember": "MARCUS VANCE (MANAGING MEMBER)",
                "wirelessPhones": ["+1-803-555-0148", "+1-803-555-0192"],
                "verifiedEmails": ["mvance@palmettoindustrial.example.com"],
                "ofacSanctionsStatus": "CLEAR (0 SDN hits)",
                "reportType": report_type,
                "upgradeUrl": "https://ceadigital.io/tools",
            },
        }


def handle_request(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    req_id = msg.get("id")

    if req_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "cea-skip-trace-owner-phone-finder",
                    "version": "1.2.0",
                },
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = msg.get("params") or {}
        tool_name = params.get("name")
        arguments = params.get("arguments") or {}
        if tool_name != "skip_trace_owner_phone_finder":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"},
            }
        data = _call_upstream(arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2),
                    }
                ],
                "isError": False,
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            resp = handle_request(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
