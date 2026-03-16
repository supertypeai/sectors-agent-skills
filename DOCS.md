# Sectors API Agent Skill - Documentation

A comprehensive skill for AI agents to fetch financial market data from the Sectors API, supporting both Indonesia Stock Exchange (IDX) and Singapore Exchange (SGX).

This repository is a **Claude Code plugin marketplace** (`sectors-agent-skills`) that also works as a standalone agent skill for backward compatibility.

---

## Overview

This repository provides AI agents with the ability to:

- Query company reports, financials, and valuations for IDX and SGX stocks
- Access historical stock prices and market indices
- Discover companies by sector, subsector, or index
- Get top performers, gainers, losers, and growth companies
- Access market data and rankings

**Supported Exchanges:**
- **IDX** (Indonesia Stock Exchange) - 19 endpoints
- **SGX** (Singapore Exchange) - 6 endpoints

---

## Quick Start for Users

### 1. Get Your API Key

Visit [https://sectors.app/api](https://sectors.app/api) to obtain your API key.

### 2. Install This Skill

Clone or copy this repository to your local machine:

```bash
git clone <repository-url> sectors-agent-skills
cd sectors-agent-skills
```

### 3. Configure Your AI Agent

Choose your AI agent and follow the integration guide below:

- [Claude Code Plugin (Recommended)](#claude-code-plugin-recommended)
- [Claude Code Integration (Standalone)](#claude-code-integration)
- [OpenCode Integration](#opencode-integration)
- [Generic AI Agent Integration](#generic-ai-agent-integration)

### 4. Verify Setup

Run the setup verification script:

```bash
python scripts/check_setup.py
```

You should see output like:
```
[ok] SECTORS_API_KEY is set (32 characters)
[ok] requests library is available
[ok] API is reachable and authenticated (148 subsectors found)

Setup is complete. Your agent can now use the Sectors API skill.
```

---

## Claude Code Plugin (Recommended)

The simplest way to use this skill with Claude Code is to install it as a plugin.

### Step 1: Install the Plugin

```bash
claude plugin install sectors-api@sectors-agent-skills
```

### Step 2: Set the API Key

```bash
claude config set env SECTORS_API_KEY your-api-key-here
```

### Step 3: Start Chatting

The `sectors-api` skill is now available in all your Claude Code sessions. Try:

- "What is the current market cap of BBCA?"
- "Show me the top 5 gainers in the LQ45 index over the last 7 days"
- "Get the quarterly financials for BBRI for the last 4 quarters"
- "What are the top dividend yield stocks in Singapore?"

### Updating the Plugin

```bash
claude plugin update sectors-api
```

### Removing the Plugin

```bash
claude plugin remove sectors-api
```

---

## Claude Code Integration

### Step 1: Set the API Key

Configure Claude Code with your Sectors API key:

```bash
claude config set env SECTORS_API_KEY your-api-key-here
```

Or add it to your Claude Code configuration file (usually at `~/.config/claude/settings.json`):

```json
{
  "env": {
    "SECTORS_API_KEY": "your-api-key-here"
  }
}
```

### Step 2: Point Claude to the Skill

When starting Claude Code from this directory, it will automatically read the `SKILL.md` file. You can also explicitly reference it:

```bash
claude --skill ./SKILL.md
```

Or within Claude Code:

```
/claude read ./SKILL.md
```

### Step 3: Start Chatting

Once configured, you can ask Claude questions like:

- "What is the current market cap of BBCA?"
- "Show me the top 5 gainers in the LQ45 index over the last 7 days"
- "Get the quarterly financials for BBRI for the last 4 quarters"
- "Compare the P/E ratios of banks in the IDX"
- "What are the top dividend yield stocks in Singapore?"

---

## OpenCode Integration

### Step 1: Set the API Key

Configure OpenCode with your Sectors API key in your configuration file (usually at `~/.config/opencode/config.json`):

```json
{
  "env": {
    "SECTORS_API_KEY": "your-api-key-here"
  }
}
```

Or set it via environment variable before starting OpenCode:

```bash
export SECTORS_API_KEY="your-api-key-here"
opencode
```

### Step 2: Load the Skill

OpenCode will automatically detect `SKILL.md` in the current directory. You can also manually load it:

```
/load-skill ./SKILL.md
```

### Step 3: Start Chatting

Ask OpenCode questions about financial data:

- "What companies are in the banking subsector?"
- "Get the company report for D05 (DBS Group)"
- "Show me IDX historical data for the last 30 days"

---

## Generic AI Agent Integration

### For AI Agent Developers

To integrate this skill with any AI agent:

#### 1. Parse the Skill File

Read and parse `SKILL.md`. The file contains:
- **YAML frontmatter** (lines between `---`) with metadata:
  - `name`: `sectors-api`
  - `description`: What the skill does
  - `license`: MIT
  - `compatibility`: Requirements
  - `allowed-tools`: Bash(python:*), Bash(pip:*), Read

#### 2. Extract Constraints

The skill has specific constraints your agent must follow:
- **ONLY** make HTTP requests to `https://api.sectors.app/v1`
- All endpoints are `GET` requests returning JSON
- **Never** hardcode or guess an API key
- Always read API key from `SECTORS_API_KEY` environment variable
- If the env var is not set, prompt the user to set it

#### 3. Implement the Skill

Your agent should:

1. **Check for API key** before making any requests:
   ```python
   import os
   api_key = os.environ.get("SECTORS_API_KEY")
   if not api_key:
       return "Please set your SECTORS_API_KEY environment variable. Get your key at https://sectors.app/api"
   ```

2. **Make authenticated requests**:
   ```python
   import requests
   
   BASE_URL = "https://api.sectors.app/v1"
   headers = {"Authorization": api_key}  # No "Bearer" prefix!
   
   response = requests.get(f"{BASE_URL}/subsectors/", headers=headers)
   data = response.json()
   ```

3. **Handle errors appropriately**:
   - 403: Invalid API key
   - 404: Resource not found
   - Other: API error

#### 4. Parse Endpoint Tables

The skill contains decision tables mapping user intents to endpoints. Your agent should:

- Parse the tables in the "Endpoint decision table" section
- Match user queries to appropriate endpoints
- Extract required and optional parameters

**Example pattern matching:**

| User Query Pattern | Endpoint |
|---|---|
| "companies in {subsector}" | `/companies/?sub_sector={sub_sector}` |
| "report for {ticker}" | `/company/report/{ticker}/` |
| "top gainers" | `/companies/top-changes/` |
| "daily price {ticker}" | `/daily/{ticker}` |

#### 5. Ticker Normalization

Your agent must normalize tickers before API calls:

| Market | Rule | Example |
|---|---|---|
| IDX | Uppercase, strip `.JK` | `bbca.jk` → `BBCA` |
| SGX | Uppercase, strip `.SI` | `d05.si` → `D05` |

#### 6. Parameter Conventions

| Convention | Rule |
|---|---|
| Dates | `YYYY-MM-DD` format |
| Subsectors | kebab-case (e.g., `banks`, `consumer-defensive`) |
| Multiple values | Comma-separated (e.g., `top_gainers,top_losers`) |
| Market cap IDX | Billion IDR (`min_mcap_billion`) |
| Market cap SGX | Million SGD (`min_mcap_million`) |

---

## For AI Agents: How to Use This Skill

### Installation Checklist

When a user wants to use this skill, follow these steps:

1. **Verify the skill files exist**:
   - Check that `SKILL.md` is present
   - Check that `scripts/check_setup.py` exists
   - Verify `references/idx-endpoints.md` and `references/sgx-endpoints.md` exist

2. **Check environment setup**:
   ```python
   import os
   if "SECTORS_API_KEY" not in os.environ:
       print("ERROR: SECTORS_API_KEY not set")
       print("\nSet it with:")
       print('  export SECTORS_API_KEY="your-api-key-here"')
       print("\nGet your API key at: https://sectors.app/api")
   ```

3. **Verify dependencies**:
   ```python
   try:
       import requests
   except ImportError:
       print("Installing requests library...")
       # Run: pip install requests
   ```

4. **Test connectivity**:
   Run the setup check script or make a test API call to `/subsectors/`

### Understanding the Skill Structure

```
sectors-agent-skills/
├── .claude-plugin/           # Marketplace manifest
│   └── marketplace.json      # Plugin catalog
├── plugins/                  # Plugin packages
│   └── sectors-api/          # The sectors-api plugin
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin manifest (version, metadata)
│       ├── skills/
│       │   └── sectors-api/
│       │       ├── SKILL.md          # Plugin skill definition
│       │       ├── assets/
│       │       │   └── endpoint-map.md
│       │       └── references/
│       │           ├── idx-endpoints.md
│       │           └── sgx-endpoints.md
│       └── scripts/
│           └── check_setup.py
├── SKILL.md              # Standalone skill definition (backward compat)
├── DOCS.md               # This file
├── README.md             # User documentation
├── assets/
│   └── endpoint-map.md   # Quick reference table
├── references/
│   ├── idx-endpoints.md  # Detailed IDX docs (19 endpoints)
│   └── sgx-endpoints.md  # Detailed SGX docs (6 endpoints)
└── scripts/
    └── check_setup.py    # Setup verification
```

### Key Sections in SKILL.md

1. **Constraints** (lines 25-30): Rules you MUST follow
2. **Setup** (lines 32-63): How to configure
3. **Endpoint decision table** (lines 81-137): Maps user needs to endpoints
4. **Common patterns** (lines 139-242): Code examples
5. **Gotchas** (lines 253-278): Important warnings

### Endpoint Categories

Your agent should understand these endpoint groups:

**Market Structure:**
- `/subsectors/` - List all subsectors
- `/industries/` - List all industries
- `/sgx/sectors/` - List SGX sectors

**Company Discovery:**
- `/companies/?sub_sector={sub_sector}` - Companies by subsector
- `/index/{index}/` - Companies in an index
- `/sgx/companies/?sector={sector}` - SGX companies by sector

**Company Details:**
- `/company/report/{ticker}/` - Full company report
- `/financials/quarterly/{ticker}/` - Quarterly financials
- `/daily/{ticker}` - Daily stock prices
- `/sgx/company/report/{ticker}` - SGX company report

**Market Data & Rankings:**
- `/companies/top-changes/` - Top gainers/losers
- `/companies/top/` - Top by metrics (P/E, dividend yield, etc.)
- `/companies/top-growth/` - Top growth companies
- `/most-traded/` - Most traded stocks
- `/sgx/companies/top/` - SGX top companies

### Authentication Pattern

```python
import os
import requests

# ALWAYS get key from environment
API_KEY = os.environ["SECTORS_API_KEY"]
BASE_URL = "https://api.sectors.app/v1"

# Authorization header is RAW KEY - no Bearer prefix
headers = {"Authorization": API_KEY}

# Make request
response = requests.get(f"{BASE_URL}/subsectors/", headers=headers)
```

### Error Handling Template

```python
response = requests.get(url, headers=headers)

if response.status_code == 403:
    return "Error: Invalid or missing API key. Please check your SECTORS_API_KEY."
elif response.status_code == 404:
    return f"Error: Resource not found: {ticker}"
elif not response.ok:
    return f"API error {response.status_code}: {response.text}"

data = response.json()
```

### Common User Queries and Endpoints

| User Asks | Use Endpoint | Parameters |
|---|---|---|
| "Market cap of BBCA" | `/company/report/{ticker}/` | `ticker=BBCA`, `sections=overview` |
| "Top 5 gainers this week" | `/companies/top-changes/` | `classifications=top_gainers`, `periods=7d`, `n_stock=5` |
| "BBRI quarterly earnings" | `/financials/quarterly/{ticker}/` | `ticker=BBRI`, `n_quarters=4` |
| "Companies in banking" | `/companies/?sub_sector={sub_sector}` | `sub_sector=banks` |
| "LQ45 companies" | `/index/{index}/` | `index=lq45` |
| "DBS Group report" | `/sgx/company/report/{ticker}` | `ticker=D05` |
| "Top dividend yield stocks" | `/companies/top/` | `classifications=dividend_yield` |
| "IDX historical data" | `/index-daily/{index_code}/` | `index_code=ihsg` |
| "BBCA stock price" | `/daily/{ticker}` | `ticker=BBCA` |

### Ticker Normalization Function

```python
def normalize_ticker(ticker, market="IDX"):
    """
    Normalize ticker symbols for API calls.
    
    Args:
        ticker: Raw ticker (e.g., "bbca.jk", "BBCA")
        market: "IDX" or "SGX"
    
    Returns:
        Normalized ticker (e.g., "BBCA", "D05")
    """
    ticker = ticker.upper()
    
    if market == "IDX":
        return ticker.replace(".JK", "")
    elif market == "SGX":
        return ticker.replace(".SI", "")
    
    return ticker
```

### Response Format Examples

**Company Report (IDX):**
```json
{
  "symbol": "BBCA",
  "company_name": "Bank Central Asia Tbk",
  "overview": {
    "market_cap": 875000000000000,
    "sector": "financials",
    "sub_sector": "banks"
  },
  "valuation": {
    "pe": 22.5,
    "pb": 4.2
  }
}
```

**Top Changes (Gainers/Losers):**
```json
{
  "top_gainers": {
    "7d": [
      {
        "symbol": "BBCA",
        "name": "Bank Central Asia Tbk",
        "price_change": 5.2,
        "last_close_price": 9500
      }
    ]
  },
  "top_losers": { ... }
}
```

**Daily Stock Price:**
```json
[
  {
    "symbol": "BBCA",
    "date": "2025-01-15",
    "close": 9500,
    "volume": 12500000
  }
]
```

---

## Technical Reference

### Base URL

```
https://api.sectors.app/v1
```

### Authentication

Header: `Authorization: <raw_api_key>`

**IMPORTANT:** Do NOT prefix with "Bearer"

### Available Indices (IDX)

`ftse`, `idx30`, `idxbumn20`, `idxesgl`, `idxg30`, `idxhidiv20`, `idxq30`, `idxv30`, `jii70`, `kompas100`, `lq45`, `sminfra18`, `srikehati`, `economic30`, `idxvesta28`

### Top Companies Classifications

**IDX:** `dividend_yield`, `total_dividend`, `revenue`, `earnings`, `market_cap`, `pb`, `pe`, `ps`

**SGX:** `dividend_yield`, `revenue`, `earnings`, `market_cap`, `pe`

**Growth:** `top_earnings_growth_gainers`, `top_earnings_growth_losers`, `top_revenue_growth_gainers`, `top_revenue_growth_losers`

**Movers:** `top_gainers`, `top_losers`

### Company Report Sections

`overview`, `valuation`, `future`, `peers`, `financials`, `dividend`, `management`, `ownership`

Use `all` or omit for all sections.

---

## Troubleshooting

### API Key Issues

**Problem:** `403 Forbidden` or "Invalid API key"

**Solutions:**
1. Verify key is set: `echo $SECTORS_API_KEY`
2. Check no extra spaces: `export SECTORS_API_KEY="$(echo $SECTORS_API_KEY | tr -d ' ')"`
3. Verify at https://sectors.app/api
4. Ensure no "Bearer" prefix in Authorization header

### Environment Variable Not Set

**Problem:** "SECTORS_API_KEY environment variable is not set"

**Solutions:**
```bash
# Set in current shell
export SECTORS_API_KEY="your-key"

# Or add to shell profile
echo 'export SECTORS_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# For Claude Code
claude config set env SECTORS_API_KEY your-key
```

### Module Not Found

**Problem:** `ImportError: No module named 'requests'`

**Solution:**
```bash
pip install requests
```

### Network Issues

**Problem:** "Cannot reach https://api.sectors.app"

**Solutions:**
1. Check internet connection
2. Verify no firewall blocking the domain
3. Try: `curl -I https://api.sectors.app/v1/subsectors/`

### Invalid Ticker

**Problem:** "Resource not found" for ticker

**Solutions:**
1. Normalize ticker: Remove `.JK` or `.SI` suffix
2. Use uppercase: `bbca` → `BBCA`
3. Check available companies in sector/index first

### Date Format Issues

**Problem:** Invalid date errors

**Solution:** Use `YYYY-MM-DD` format (e.g., `2025-01-15`)

---

## Example Conversations

### Example 1: Simple Query

**User:** "What's the market cap of Bank Central Asia?"

**Agent:** ( internally normalizes "Bank Central Asia" to ticker "BBCA", calls `/company/report/BBCA/?sections=overview` )

**Agent Response:** "Bank Central Asia (BBCA) has a market cap of approximately Rp 875 trillion."

### Example 2: Comparative Analysis

**User:** "Compare the P/E ratios of the top 3 banks"

**Agent:** ( calls `/companies/?sub_sector=banks`, then gets reports for top 3, extracts valuation.pe )

**Agent Response:** "Here are the P/E ratios for the top 3 banks by market cap:
- BBCA: 22.5
- BBRI: 18.3
- BMRI: 15.7"

### Example 3: Market Movers

**User:** "Show me the biggest gainers this week in the LQ45"

**Agent:** ( calls `/companies/top-changes/?classifications=top_gainers&periods=7d&n_stock=5` and filters by LQ45 companies )

**Agent Response:** "Top 5 gainers in LQ45 over the last 7 days:
1. ABCD +12.5%
2. EFGH +8.3%
3. ..."

### Example 4: Historical Data

**User:** "What was BBCA's stock price on January 1, 2025?"

**Agent:** ( calls `/daily/BBCA?start=2025-01-01&end=2025-01-01` )

**Agent Response:** "On January 1, 2025, BBCA closed at Rp 9,250 with a volume of 12.5 million shares."

**Ready to start?** Set your API key and ask your AI agent about financial data!
