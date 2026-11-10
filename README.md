# Skip Trace & Property / LLC Owner Phone Finder (Python CLI, SDK & MCP Server)

[![Apify Store](https://img.shields.io/badge/Apify_Store-cea__digital%2Fskip--trace--owner--phone--finder-00C853?style=flat-square)](https://apify.com/cea_digital/skip-trace-owner-phone-finder)
[![Direct Unified Key](https://img.shields.io/badge/Direct_Unified_Key-%242_Tripwire_%7C_%2429%2Fmo-2563EB?style=flat-square)](https://ceadigital.io/tools)
[![Run in Postman](https://img.shields.io/badge/Run_in_Postman-v2.1_Collection-FF6C37?style=flat-square&logo=postman&logoColor=white)](https://ceadigital.io/templates/postman-collection.json)
[![Smithery MCP](https://smithery.ai/badge/@ceadigital/skip-trace-owner-phone-finder-python)](https://smithery.ai/server/@ceadigital/skip-trace-owner-phone-finder-python)
[![Glama MCP](https://img.shields.io/badge/Glama_MCP-Grade_A_TDQS-8B5CF6?style=flat-square)](https://glama.ai/mcp/servers/@ceadigital/skip-trace-owner-phone-finder-python)
[![Zero Charge on Misses](https://img.shields.io/badge/Miss_Guarantee-%240.00_on_Unfound_Leads-10B981?style=flat-square)](https://ceadigital.io/tools)

Pierce anonymous real estate LLCs (`PALMETTO INDUSTRIAL HOLDINGS LLC` -> Managing Member human name), resolve verified wireless mobile phone numbers + deliverable emails, enrich with live **GLEIF LEI** & **U.S. Census Geocoder** coordinates, and run **U.S. Treasury OFAC SDN** KYB compliance checks in `<2s` over pure HTTP (`Accept-Encoding: gzip, deflate`, zero headless browser).

---

## 1-Click Ecosystem & No-Code Integrations

| Platform / Channel | Direct Link |
| :--- | :--- |
| **Direct $29/mo Stripe API Key & $2 Tripwire Pass (Free 1-Row Preview)** | **[https://ceadigital.io/tools](https://ceadigital.io/tools)** |
| **Apify Store Actor (`cea_digital/skip-trace-owner-phone-finder`)** | **[https://apify.com/cea_digital/skip-trace-owner-phone-finder](https://apify.com/cea_digital/skip-trace-owner-phone-finder)** |
| **Run in Postman (Public Collection v2.1)** | **[https://ceadigital.io/templates/postman-collection.json](https://ceadigital.io/templates/postman-collection.json)** |
| **1-Click Google Sheets Custom Function (`=SKIPTRACE(A2, B2)`)** | **[https://ceadigital.io/templates/Code.gs](https://ceadigital.io/templates/Code.gs)** |
| **1-Click n8n Native Workflow Template (`.workflow.json`)** | **[https://ceadigital.io/templates/skip-trace-owner-phone-finder.workflow.json](https://ceadigital.io/templates/skip-trace-owner-phone-finder.workflow.json)** |
| **Clay.com HTTP API Column Blueprints** | **[https://ceadigital.io/templates/clay-http-column-blueprints.json](https://ceadigital.io/templates/clay-http-column-blueprints.json)** |
| **Smithery MCP Registry** | **[https://smithery.ai/server/@ceadigital/skip-trace-owner-phone-finder-python](https://smithery.ai/server/@ceadigital/skip-trace-owner-phone-finder-python)** |
| **Glama MCP Server Directory** | **[https://glama.ai/mcp/servers/@ceadigital/skip-trace-owner-phone-finder-python](https://glama.ai/mcp/servers/@ceadigital/skip-trace-owner-phone-finder-python)** |

---

## Quickstart #1 — Direct Unified API Key (`https://ceadigital.io/tools`)

Bypass platform monthly minimums with a single **`cea_live_`** Unified API Key (**$2.00 One-Time 100-Hit Tripwire Pass** or **$29/mo Growth Plan for 5,000 hits** across all 4 CEA Digital tools):

```bash
export CEA_API_KEY="cea_live_your_key_here"
python skip_trace_cli.py \
  --name "PALMETTO INDUSTRIAL HOLDINGS LLC" \
  --address "1201 Main St Ste 1980, Columbia, SC 29201" \
  --report-type full_kyb_guarantor_diligence
```

Or via `curl`:

```bash
curl -sS -X POST "https://ceadigital.io/v1/tools/skip-trace-owner-phone-finder" \
  -H "Authorization: Bearer $CEA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "companyOrOwnerNames": ["PALMETTO INDUSTRIAL HOLDINGS LLC"],
    "addresses": ["1201 Main St Ste 1980, Columbia, SC 29201"],
    "reportType": "pierce_llc_and_skip_trace",
    "includeLiens": true
  }' | jq .
```

---

## Quickstart #2 — Apify Store (`cea_digital/skip-trace-owner-phone-finder`)

Run on Apify Pay-Per-Event (`$0.004/lead` on Bronze+ plans, `$0.00` on misses) or chain directly to `maxcopell/zillow-detail-scraper` / `compass/crawler-google-places` via `zillowOrMapsDatasetId`:

```bash
export APIFY_TOKEN="apify_api_your_token_here"
python skip_trace_cli.py \
  --apify \
  --name "SUNBELT DISTRESSED ASSETS LLC" \
  --address "400 E Van Buren St, Phoenix, AZ 85004"
```

```bash
curl -sS -X POST "https://api.apify.com/v2/acts/cea_digital~skip-trace-owner-phone-finder/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "companyOrOwnerNames": ["SUNBELT DISTRESSED ASSETS LLC"],
    "addresses": ["400 E Van Buren St, Phoenix, AZ 85004"],
    "reportType": "pierce_llc_and_skip_trace"
  }' | jq .
```

---

## Quickstart #3 — Model Context Protocol (MCP) for Claude, Cursor, Smithery & Glama

### Remote Streamable-HTTP MCP (Zero Install)
```bash
claude mcp add --transport http ceadigital-b2a https://ceadigital.io/mcp
```

### Smithery 1-Click Install
```bash
npx -y @smithery/cli install @ceadigital/skip-trace-owner-phone-finder-python --client claude
```

### Local Stdio MCP Server (`mcp_server.py`)
```json
{
  "mcpServers": {
    "cea-skip-trace": {
      "command": "python3",
      "args": ["/path/to/skip-trace-owner-phone-finder-python/mcp_server.py"],
      "env": {
        "CEA_API_KEY": "cea_live_optional_key_or_blank_for_free_preview"
      }
    }
  }
}
```

---

## License

MIT License — Copyright (c) 2026 CEA Digital ([ceadigital.io](https://ceadigital.io))
