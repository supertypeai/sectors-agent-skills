# Sectors Agent Skills

A set of skills and utilities for building agents that interact with financial market data from the Sectors API, supporting both Indonesia Stock Exchange (IDX) and Singapore Exchange (SGX).

This repository serves as both a **Claude Code plugin marketplace** and a standalone agent skill.

## Overview

This repository provides tools and documentation to integrate with the Sectors API, which offers comprehensive financial data including:
- **IDX (Indonesia Stock Exchange)**: Company information, financial metrics, indices, and market data
- **SGX (Singapore Exchange)**: Company information, sectors, and market data

## Getting Started

### Option A: Install as a Claude Code Plugin (Recommended)

The easiest way to use this skill is to install it as a Claude Code plugin:

```bash
claude plugin install sectors-api@sectors-agent-skills
```

Then set your API key:

```bash
claude config set env SECTORS_API_KEY your-api-key-here
```

That's it. The `sectors-api` skill will be available in all your Claude Code sessions.

### Option B: Use as a Standalone Skill

If you prefer to use the repository directly (or use a non-Claude Code agent), follow the steps below.

### 1. Get an API Key

Get your API key from: https://sectors.app/api

### 2. Set Up Environment

Create a `.env` file in the root directory with your API key:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```
SECTORS_API_KEY=your-api-key-here
```

Alternatively, export it in your terminal:

```bash
export SECTORS_API_KEY="your-api-key-here"
```

Or add it to your shell profile:

```bash
echo 'export SECTORS_API_KEY="your-api-key-here"' >> ~/.bashrc
# or for zsh:
echo 'export SECTORS_API_KEY="your-api-key-here"' >> ~/.zshrc
```

### 3. Verify Setup

Run the setup verification script to ensure your configuration is correct:

```bash
python scripts/check_setup.py
```

This script will:
- Check that `SECTORS_API_KEY` is set
- Verify the requests library is installed
- Test connectivity to the API
- Validate your API key

## API Documentation

### Endpoint Reference

See [assets/endpoint-map.md](assets/endpoint-map.md) for a complete list of available API endpoints with parameter descriptions.

### Supported Exchanges

- **IDX Endpoints**: See [references/idx-endpoints.md](references/idx-endpoints.md)
- **SGX Endpoints**: See [references/sgx-endpoints.md](references/sgx-endpoints.md)

### Parameter Conventions

| Convention | Rule |
|---|---|
| Dates | `YYYY-MM-DD` format |
| Tickers (IDX) | Uppercase, no `.JK` suffix |
| Tickers (SGX) | Uppercase, no `.SI` suffix |
| Subsectors / sectors | kebab-case (e.g. `banks`, `consumer-defensive`) |
| Multiple values | Comma-separated string |
| Market cap (IDX) | Billion IDR |
| Market cap (SGX) | Million SGD |
| Auth header | `Authorization: <raw_api_key>` (no Bearer prefix) |

## Key Features

- **Subsectors & Industries**: Get classification data for both exchanges
- **Company Data**: Query companies by sector, subsector, or index
- **Financial Data**: Access quarterly financials, company reports, and segments
- **Market Analytics**: Top movers, most traded, top growth companies
- **Index Data**: Historical index data and total market cap metrics
- **Daily Transactions**: Historical trading data by ticker

## Requirements

- Python 3.8 or higher
- `requests` library (`pip install requests`)

## Environment Variables

- `SECTORS_API_KEY`: Your Sectors API authentication key (required)

## Project Structure

```
.
├── .claude-plugin/          # Marketplace manifest
│   └── marketplace.json     # Plugin catalog for this marketplace
├── plugins/                 # Plugin packages
│   └── sectors-api/         # The sectors-api plugin
│       ├── .claude-plugin/
│       │   └── plugin.json  # Plugin manifest (version, metadata)
│       ├── skills/
│       │   └── sectors-api/
│       │       ├── SKILL.md         # Plugin skill definition
│       │       ├── assets/
│       │       │   └── endpoint-map.md
│       │       └── references/
│       │           ├── idx-endpoints.md
│       │           └── sgx-endpoints.md
│       └── scripts/
│           └── check_setup.py
├── SKILL.md                 # Standalone skill definition (backward compat)
├── assets/                  # Quick reference guides
│   └── endpoint-map.md      # All endpoints at a glance
├── references/              # Detailed endpoint documentation
│   ├── idx-endpoints.md     # Indonesia Stock Exchange endpoints
│   └── sgx-endpoints.md     # Singapore Exchange endpoints
├── scripts/                 # Utility scripts
│   └── check_setup.py       # Setup verification script
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── DOCS.md                  # Detailed documentation
└── README.md                # This file
```

## Security

- **Never hardcode API keys** in your code
- Always read the API key from the `SECTORS_API_KEY` environment variable
- Use `.env.example` as a template for configuration
- The `.env` file (containing your actual API key) is automatically excluded from version control

## Support

For issues, questions, or feedback:
1. Check the endpoint reference documents in the `references/` directory
2. Review the setup script at `scripts/check_setup.py`
3. Ensure your API key is valid at https://sectors.app/api

## License

See LICENSE file for details (if applicable).
