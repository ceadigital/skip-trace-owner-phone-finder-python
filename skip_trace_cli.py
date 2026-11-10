#!/usr/bin/env python3
"""
CLI & SDK for CEA Digital Actor #1: Skip Trace & Property / LLC Owner Phone Finder.
Supports both Direct Unified Key (`https://ceadigital.io/tools`) and Apify Store (`cea_digital/skip-trace-owner-phone-finder`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx

DIRECT_ENDPOINT = "https://ceadigital.io/v1/tools/skip-trace-owner-phone-finder"
APIFY_ENDPOINT = "https://api.apify.com/v2/acts/cea_digital~skip-trace-owner-phone-finder/run-sync-get-dataset-items"


def run_skip_trace(
    names: list[str],
    addresses: list[str],
    report_type: str = "pierce_llc_and_skip_trace",
    include_liens: bool = True,
    use_apify: bool = False,
    api_key: str | None = None,
) -> dict[str, Any] | list[dict[str, Any]]:
    payload = {
        "companyOrOwnerNames": names,
        "addresses": addresses,
        "reportType": report_type,
        "includeLiens": include_liens,
    }
    headers = {"Accept-Encoding": "gzip, deflate", "Content-Type": "application/json"}

    with httpx.Client(timeout=30.0, headers=headers) as client:
        if use_apify:
            token = api_key or os.environ.get("APIFY_TOKEN", "").strip()
            if not token:
                raise RuntimeError("Missing APIFY_TOKEN. Set APIFY_TOKEN or use https://ceadigital.io/tools with CEA_API_KEY.")
            resp = client.post(f"{APIFY_ENDPOINT}?token={token}", json=payload)
            resp.raise_for_status()
            return resp.json()

        key = api_key or os.environ.get("CEA_API_KEY", "").strip()
        if not key:
            raise RuntimeError("Missing CEA_API_KEY. Claim a $2 Tripwire Pass or $29/mo Growth Key at https://ceadigital.io/tools")
        resp = client.post(DIRECT_ENDPOINT, headers={"Authorization": f"Bearer {key}"}, json=payload)
        resp.raise_for_status()
        return resp.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Pierce anonymous LLCs & skip-trace property owner wireless phones.")
    parser.add_argument("--name", action="append", default=[], help="LLC or property owner name (repeatable)")
    parser.add_argument("--address", action="append", default=[], help="Street address (repeatable)")
    parser.add_argument("--report-type", default="pierce_llc_and_skip_trace", choices=["skip_trace_only", "pierce_llc_and_skip_trace", "full_kyb_guarantor_diligence"])
    parser.add_argument("--apify", action="store_true", help="Route via Apify Store (cea_digital/skip-trace-owner-phone-finder)")
    parser.add_argument("--api-key", default=None, help="Explicit CEA_API_KEY or APIFY_TOKEN")
    args = parser.parse_args()

    names = args.name or ["PALMETTO INDUSTRIAL HOLDINGS LLC"]
    addresses = args.address or ["1201 Main St Ste 1980, Columbia, SC 29201"]
    try:
        res = run_skip_trace(
            names=names,
            addresses=addresses,
            report_type=args.report_type,
            use_apify=args.apify,
            api_key=args.api_key,
        )
        print(json.dumps(res, indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
