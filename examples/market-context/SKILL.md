---
name: market-context
description: |
  Use this skill when the user wants live crypto market context alongside (or to explain) their affiliate performance — total market cap, 24h volume, BTC/ETH dominance — e.g. "why did commission drop yesterday?", "is it the market or my invitees?", "market overview", "大盘怎么样", "هل السوق هو السبب؟". Pulls real-time global metrics from the CoinMarketCap API and compares them with the affiliate node's numbers. Do NOT use for per-user analysis (use `whale-deep-dive`).
---

# Market context — is it the market or my node?

> "Commission is down 30% — is the whole market down?"

Combines live global market metrics from CoinMarketCap with the affiliate node's own
performance so the user can tell a market-wide move from a node-specific problem.

## Setup

1. Get a free API key at <https://pro.coinmarketcap.com> (Basic plan includes this endpoint).
2. Export it — never commit it (`.env` is already git-ignored):

   ```bash
   export CMC_API_KEY=your-key
   ```

## When to use this skill

- User asks why commission / volume moved and wants to rule out the market
- User asks for a "market overview" before a community post or campaign
- As an optional context line in `daily-briefing`

## What the agent does

### 1. Live market metrics (CoinMarketCap)

```bash
python3 examples/market-context/scripts/cmc_global_metrics.py --json
```

Wraps `GET https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest` and prints:

```json
{"currency":"USD","total_market_cap":3.1e12,"total_volume_24h":1.2e11,
 "market_cap_change_24h_pct":-1.5,"volume_change_24h_pct":-22.4,
 "btc_dominance":57.1,"eth_dominance":12.3,"active_cryptocurrencies":9000,
 "active_exchanges":700,"last_updated":"2026-10-02T00:00:00.000Z"}
```

Pass `--convert EUR` (one symbol on the Basic plan) for another quote currency.

### 2. Node performance for the same window

```json
{
  "name": "okx-affiliate-performance-summary",
  "arguments": {
    "begin": "<yesterday 00:00:00 UTC in ms>",
    "end":   "<yesterday 23:59:59 UTC in ms>"
  }
}
```

```json
{ "name": "okx-affiliate-performance-summary", "arguments": { "periodType": "last_7d" } }
```

## Sample output

```
🌍 Market (CoinMarketCap, 02:36 UTC)
   Cap $3.10T (-1.5% 24h) · Volume $120B (-22% 24h) · BTC dom 57.1%

📊 Your node (yesterday vs 7d avg)
   Volume -24% · Commission -30%

✅ Volume drop tracks the market (-22% vs -24%) — not a node problem.
⚠️ Commission fell 6 pts more than volume → mix shifted to lower-fee users; check top 10.
```

## Insights to extract

- **Node vs market volume delta** — within ~5 pts ⇒ market-driven; much worse ⇒ node-specific
- **Rising BTC dominance** — risk-off; altcoin-heavy invitees usually trade less
- **Market volume up but node flat** — activation problem; hand off to `high-potential-invitees`

## Notes

- Data refreshes about every 5 minutes; each call costs 1 credit. Cache within a session.
- On error the script exits non-zero with CoinMarketCap's `status.error_message`.

## Recommended follow-ups

- "Who stopped trading even though the market was up?" → `churn-rescue`
- "Show the 3-month trend against the market" → `acquisition-trends`
