---
name: sectors-api
description: >
  Query financial market data from the Sectors API (api.sectors.app) for IDX
  (Indonesia), SGX (Singapore), KLSE (Malaysia) equities, and Indonesian
  mining sector data. Use when the user asks about stock prices, company
  reports, financials, market indices, top movers, dividends, earnings,
  market cap, broker activity, filings, news, or mining companies/licenses/
  production. Only calls https://api.sectors.app. Python with requests.
license: MIT
compatibility: >
  Requires Python 3.8+ with the requests library. Requires the SECTORS_API_KEY
  environment variable to be set. Requires network access to https://api.sectors.app.
metadata:
  author: supertype
  version: "2.1"
allowed-tools: Bash(python:*) Bash(pip:*) Read
---

# Sectors API

Query IDX, SGX, KLSE, and mining-sector financial data through the Sectors
REST API (`/v2`). Full docs: https://sectors.app/api

## Constraints

- ONLY call `https://api.sectors.app/v2`. Never any other domain.
- All endpoints are `GET`, returning JSON.
- Never hardcode or guess an API key — always read `SECTORS_API_KEY` from the environment. If unset, tell the user to `export SECTORS_API_KEY="your-api-key-here"` (get one at https://sectors.app/api).

## Setup

```bash
pip install requests
python scripts/check_setup.py   # optional: verifies key + connectivity
```

## Request pattern

Every call has this exact shape — only the path and `params` change per endpoint:

```python
import os
import requests

API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v2"
headers = {"Authorization": API_KEY}  # raw key — NOT "Bearer <key>"

resp = requests.get(f"{BASE_URL}/company/report/BBCA/", headers=headers, params={"sections": "overview,valuation"})
if resp.status_code == 403:
    raise ValueError("Invalid or missing API key. Ensure SECTORS_API_KEY is set correctly.")
if not resp.ok:
    raise RuntimeError(f"API error {resp.status_code}: {resp.text}")
data = resp.json()
```

## Endpoint decision table

Pick the endpoint **key** for what the user needs, then resolve exact params via
"Getting exact parameters" below. The table is auto-generated from the schema;
the "User wants" column is maintained in `scripts/data/intent_map.json`.

<!-- GENERATED:decision-table:start -->
| Market | User wants | Endpoint key | Required params |
|---|---|---|---|
| IDX | Filter/screen companies (SQL-like / natural language) | `Companies Screener` | none |
| IDX | Free float by sector/subsector/industry | `Free Float Market Analysis` | none |
| IDX | Companies with segment data | `Companies with Revenue Segments` | none |
| IDX | List all industries | `Industries` | none |
| IDX | News/filing tags | `News Tags` | none |
| IDX | Quarterly financial report dates | `Quarterly Financial Dates` | `symbol` |
| IDX | List all subindustries | `Subindustries` | none |
| IDX | List all subsectors | `Subsectors` | none |
| IDX | Quarterly financials | `Company Quarterly Financials` | `symbol` |
| IDX | Full company report | `Company Report` | `symbol` |
| IDX | Revenue/cost segments | `Company Revenue Segments` | `symbol` |
| IDX | Corporate actions (splits, dividends, AGM, etc.) | `Corporate Actions` | `symbol` |
| IDX | Shareholders composition | `Shareholders Composition` | `symbol` |
| IDX | Subsector report | `Subsector Report` | `sub_sector` |
| IDX | Daily price/volume/market cap | `Daily Transaction Data` | `symbol` |
| IDX | IDX total market cap | `IDX Market Summary` | none |
| IDX | Index daily price history | `Index Daily Transaction Data` | `index_code` |
| IDX | Most traded stocks | `Most Traded Stocks` | none |
| IDX | Top gainers/losers | `Top Company Movers` | none |
| IDX | Listing/IPO performance | `Company IPO & Listing Performance` | `symbol` |
| IDX | Insider filings | `Company Filings` | none |
| IDX | News articles (IDX or mining) | `News Articles` | none |
| IDX | Stock suspensions | `Stock Suspensions` | none |
| IDX | Per-broker daily activity | `Broker Activity By Code` | `broker_code` |
| IDX | Per-symbol broker activity | `Broker Activity Per Symbol` | `symbol` |
| IDX | Broker registry | `Broker Registry` | none |
| IDX | Daily net foreign inflow | `Daily Net Foreign Inflow` | `symbol` |
| IDX | Per-broker top accumulations/distributions | `Top Accumulations and Distributions Per Broker` | `broker_code` |
| IDX | Top brokers daily ranking | `Top Brokers Daily Ranking` | none |
| IDX | Per-symbol top buyers/sellers | `Top Buyers and Sellers Per Symbol` | `symbol` |
| SGX | Filter/screen SGX companies | `SGX Companies Screener` | none |
| SGX | List SGX sectors | `List all SGX sectors` | none |
| SGX | SGX news tags | `SGX News Tags` | none |
| SGX |  | `SGX Subsectors` | none |
| SGX | Full SGX company report | `Full company report for an SGX-listed symbol` | `symbol` |
| SGX | SGX daily price/volume | `SGX Daily Price Data` | `symbol` |
| SGX | SGX share buybacks | `SGX Share Buybacks` | none |
| SGX | SGX short-sell activity | `SGX Short Sell` | none |
| SGX | Top SGX companies by classification | `Top SGX companies by classification` | none |
| SGX | SGX insider filings | `SGX Insider Filings` | none |
| SGX | SGX news | `SGX News` | none |
| KLSE | Full KLSE company report | `Full company report for a KLSE-listed symbol` | `symbol` |
| KLSE | KLSE companies by sector | `List KLSE companies filtered by sector` | `sector` |
| KLSE | List KLSE sectors | `List all KLSE sectors` | none |
| KLSE | Top KLSE companies by classification | `Top KLSE companies by classification` | none |
| Mining | List/search mining companies | `List Mining Companies` | none |
| Mining | Mining company detail | `Mining Company Detail` | `slug` |
| Mining | Mining company financials | `Mining Company Financials` | `slug` |
| Mining | Mining company ownership (parents/subsidiaries) | `Mining Company Ownership` | `slug` |
| Mining | Mining company production performance | `Mining Company Performance` | `slug` |
| Mining | Commodity price history | `Commodity Price History` | `commodity_name` |
| Mining | Mining company sales destinations | `Company Sales Destinations` | `slug` |
| Mining | Global commodity data by country | `Global Commodity Data` | none |
| Mining | List commodities | `List Commodities` | none |
| Mining | Top export destinations | `Top Export Destinations` | `commodity_type`, `year` |
| Mining | Mining site detail | `Mining Site Detail` | `slug` |
| Mining | Mining sites (list/filter) | `Mining Sites` | none |
| Mining | Resources & reserves by province | `Resources & Reserves Detail` | `province` |
| Mining | National resources & reserves index | `Resources & Reserves Index` | none |
| Mining | Total national commodity production | `Total Commodity Production` | `commodity_type` |
| Mining | Mining contracts (owner/contractor) | `Mining Contracts` | none |
| Mining | Mining license auction detail | `Mining License Auction Detail` | `wiup_code` |
| Mining | Mining license auctions (list/filter) | `Mining License Auctions` | none |
| Mining | Mining licenses (list/filter) | `Mining Licenses` | none |
<!-- GENERATED:decision-table:end -->

## Getting exact parameters

1. Search the matching reference file for the line containing `"key": "<endpoint-key>"`:
   - IDX -> `references/idx-endpoints.jsonl`
   - SGX -> `references/sgx-endpoints.jsonl`
   - KLSE -> `references/klse-endpoints.jsonl`
   - Mining -> `references/mining-endpoints.jsonl`
2. That line is one complete JSON object — the full spec (path, params with types/defaults/enums, response shape).
3. Do not guess params from memory. If the key isn't in the decision table, the endpoint doesn't exist.

## Ticker normalization

| Market | Rule | Example |
|---|---|---|
| IDX | Uppercase, strip `.JK` suffix | `bbca.jk` -> `BBCA` |
| SGX | Uppercase, strip `.SI` suffix | `d05.si` -> `D05` |
| KLSE | Numeric 4-digit code, no suffix | `1155` |

Always normalize before passing to an endpoint.

## Gotchas

1. **Auth**: `Authorization: <raw_key>`. Never `Bearer`.
2. **Dates**: always `YYYY-MM-DD`.
3. **90-day cap**: time-series endpoints (`Daily Transaction Data`, `Most Traded Stocks`, `Index Daily Transaction Data`, `IDX Market Summary`, `SGX Daily Price Data`, `Broker Activity By Code`, `Daily Net Foreign Inflow`, etc.) silently clamp wider ranges to the most recent 90 days ending at `end`. A future `end` returns 400.
4. **Kebab-case** for sector/subsector values: `banks`, `consumer-defensive` — not camelCase/snake_case.
5. **Nested responses**: ranking endpoints (`Top Company Movers`, `Most Traded Stocks`, `Top SGX companies by classification`, `Top KLSE companies by classification`) key results by classification/date, sometimes by period too, e.g. `data["top_gainers"]["7d"]`, `data["2025-01-15"]`. Always navigate every level.
6. **Market cap units differ**: IDX is billion IDR (`min_mcap_billion`); SGX/KLSE is million SGD/MYR (`min_mcap_million`).
7. **`Company Report`'s `sections` param**: comma-separated; omit for all sections (costs 1 credit/section — 8 for IDX, 4 for SGX/KLSE). Valid values are in that endpoint's `references/idx-endpoints.jsonl` entry.
8. **`Company Quarterly Financials`' `approx`**: defaults to `true` (nearest quarter if `report_date` has no exact match). Set `false` to require an exact match.
9. **Screener query modes are mutually exclusive**: `q` (natural language, 3 credits) overrides `where`/`order_by`/`limit`/`offset` (structured, 1 credit) when present.
10. **Mining endpoints key on `slug`, not ticker**: discover slugs via `List Mining Companies` or `Mining Sites` first.
