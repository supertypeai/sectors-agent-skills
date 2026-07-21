# Sectors API Agent Skill

Query Indonesia (IDX), Singapore (SGX), Malaysia (KLSE), and Indonesian mining sector financial data through the [Sectors API](https://sectors.app/api).

## Get an API Key

Get your free API key at **[https://sectors.app/api](https://sectors.app/api)**.

## Install & Configure

### Claude Code (Recommended)

```bash
claude plugin marketplace add supertypeai/sectors-agent-skills
claude plugin install sectors-api@sectors-agent-skills
```

Then set your API key in `~/.claude/settings.json`:

```json
{ "env": { "SECTORS_API_KEY": "your-api-key-here" } }
```

Done. The `sectors-api` skill is available in all Claude Code sessions.

### Codex CLI

```bash
codex plugin marketplace add supertypeai/sectors-agent-skills
```

Then in a Codex CLI session, run `/plugins` to browse your marketplace sources and install the `sectors-api` plugin.

Add to `~/.codex/config.toml`:

```toml
[shell_environment_policy.set]
SECTORS_API_KEY = "your-api-key-here"
```

> ⚠️ Codex strips env vars containing `KEY`, `SECRET`, or `TOKEN` by default.
> `shell_environment_policy.set` injects after that filter — the reliable way.

**Alternative — manual symlink:**

```bash
git clone https://github.com/supertypeai/sectors-agent-skills.git
mkdir -p .agents/skills
ln -s /path/to/sectors-agent-skills/skills/sectors-api .agents/skills/sectors-api
```

### Cursor

In Cursor Agent chat, install from the plugin marketplace:

```text
/add-plugin sectors-api
```

Or add the marketplace directly:

```bash
git clone https://github.com/supertypeai/sectors-agent-skills.git
```

then point Cursor's plugin marketplace at the local checkout (or the repo URL once published), and install `sectors-api`. Set your API key via `~/.zshrc`/`~/.bashrc`:

```bash
export SECTORS_API_KEY="your-api-key-here"
```

### Antigravity CLI (`agy`)

```bash
agy plugin install https://github.com/supertypeai/sectors-agent-skills
```

Verify with `agy plugin list`. For a local checkout:

```bash
git clone https://github.com/supertypeai/sectors-agent-skills.git
agy plugin install ./sectors-agent-skills
```

Add to your shell profile (`~/.zshrc`, `~/.bashrc`):

```bash
export SECTORS_API_KEY="your-api-key-here"
```

## What You Can Ask

After install, try queries like:

- "What is the current market cap of BBCA?"
- "Show me the top 5 gainers on IDX this week"
- "Get the quarterly financials for BBRI"
- "Compare P/E ratios of banks in the IDX"
- "What are the top dividend stocks in Singapore?"
- "List mining companies in Indonesia with their production data"
- "Show me the KLSE company report for 1155"

For the full endpoint list, ask your agent to check `SKILL.md`'s decision table.

## Requirements

- Python 3.8+ with `requests` (`pip install requests`)
- Network access to `https://api.sectors.app`

## Detailed Docs

See [DOCS.md](DOCS.md) for per-harness walkthroughs, troubleshooting, example conversations, and developer reference.
