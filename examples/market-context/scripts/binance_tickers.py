#!/usr/bin/env python3
"""Fetch live 24h spot tickers from the Binance public market-data API.

Stdlib only — no third-party deps, works on any Python 3.8+. No API key needed.

Usage:
    python3 binance_tickers.py                          # BTC, ETH, BNB, SOL, XRP vs USDT
    python3 binance_tickers.py BTCUSDT DOGEUSDT         # custom symbols
    python3 binance_tickers.py --json                   # compact JSON for an agent to parse
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

# api.binance.com returns HTTP 451 from restricted regions (e.g. US); the
# data-api.binance.vision mirror serves the same public market data.
HOSTS = ("https://api.binance.com", "https://data-api.binance.vision")
PATH = "/api/v3/ticker/24hr"
DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT")
_USER_AGENT = "okx-affiliate-market-context/1.0"


def fetch(symbols: list[str]) -> list[dict]:
    query = urllib.parse.urlencode({"symbols": json.dumps(symbols, separators=(",", ":"))})
    last_err = None
    for host in HOSTS:
        req = urllib.request.Request(f"{host}{PATH}?{query}", headers={"User-Agent": _USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (403, 451):  # region-blocked — try the next host
                last_err = f"HTTP {e.code} from {host}"
                continue
            try:
                msg = json.load(e).get("msg") or e.reason
            except ValueError:
                msg = e.reason
            raise SystemExit(f"Binance HTTP {e.code}: {msg}")
        except urllib.error.URLError as e:
            last_err = f"{host}: {e.reason}"
    raise SystemExit(f"Binance unreachable ({last_err})")


def summarize(t: dict) -> dict:
    return {
        "symbol": t["symbol"],
        "last_price": float(t["lastPrice"]),
        "change_24h_pct": float(t["priceChangePercent"]),
        "high_24h": float(t["highPrice"]),
        "low_24h": float(t["lowPrice"]),
        "quote_volume_24h": float(t["quoteVolume"]),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbols", nargs="*", default=list(DEFAULT_SYMBOLS), help="e.g. BTCUSDT ETHUSDT")
    p.add_argument("--json", action="store_true", help="print compact JSON instead of text")
    args = p.parse_args()

    rows = [summarize(t) for t in fetch([s.upper() for s in args.symbols])]

    if args.json:
        print(json.dumps(rows, separators=(",", ":")))
        return

    print(f"{'Symbol':<10} {'Last':>14} {'24h %':>8} {'24h volume (quote)':>20}")
    for r in rows:
        print(f"{r['symbol']:<10} {r['last_price']:>14,.4f} {r['change_24h_pct']:>+7.2f}% {r['quote_volume_24h']:>20,.0f}")


if __name__ == "__main__":
    main()
