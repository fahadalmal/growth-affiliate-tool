#!/usr/bin/env python3
"""Fetch live global crypto market metrics from CoinMarketCap.

Stdlib only — no third-party deps, works on any Python 3.8+.

Usage:
    export CMC_API_KEY=...            # https://pro.coinmarketcap.com (Basic plan is free)
    python3 cmc_global_metrics.py             # human-readable summary, USD
    python3 cmc_global_metrics.py --json      # compact JSON for an agent to parse
    python3 cmc_global_metrics.py --convert EUR
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
_USER_AGENT = "okx-affiliate-market-context/1.0"


def fetch(api_key: str, convert: str = "USD") -> dict:
    url = f"{ENDPOINT}?{urllib.parse.urlencode({'convert': convert})}"
    req = urllib.request.Request(
        url,
        headers={
            "X-CMC_PRO_API_KEY": api_key,
            "Accept": "application/json",
            "User-Agent": _USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as e:
        # CMC returns a JSON status block even on 4xx; surface its message.
        try:
            msg = json.load(e).get("status", {}).get("error_message") or e.reason
        except ValueError:
            msg = e.reason
        raise SystemExit(f"CoinMarketCap HTTP {e.code}: {msg}")

    status = body.get("status", {})
    if status.get("error_code"):
        raise SystemExit(f"CoinMarketCap error {status['error_code']}: {status.get('error_message')}")
    return body["data"]


def summarize(data: dict, convert: str) -> dict:
    quote = data["quote"][convert]
    return {
        "currency": convert,
        "total_market_cap": quote["total_market_cap"],
        "total_volume_24h": quote["total_volume_24h"],
        "market_cap_change_24h_pct": quote.get("total_market_cap_yesterday_percentage_change"),
        "volume_change_24h_pct": quote.get("total_volume_24h_yesterday_percentage_change"),
        "btc_dominance": data["btc_dominance"],
        "eth_dominance": data["eth_dominance"],
        "active_cryptocurrencies": data["active_cryptocurrencies"],
        "active_exchanges": data["active_exchanges"],
        "last_updated": data["last_updated"],
    }


def _pct(v) -> str:
    return "n/a" if v is None else f"{v:+.2f}%"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--convert", default="USD", help="quote currency symbol (default USD)")
    p.add_argument("--json", action="store_true", help="print compact JSON instead of text")
    args = p.parse_args()

    api_key = os.environ.get("CMC_API_KEY")
    if not api_key:
        sys.exit("CMC_API_KEY is not set. Get a free key at https://pro.coinmarketcap.com")

    convert = args.convert.upper()
    s = summarize(fetch(api_key, convert), convert)

    if args.json:
        print(json.dumps(s, separators=(",", ":")))
        return

    print(f"Total market cap : {s['total_market_cap']:,.0f} {convert} ({_pct(s['market_cap_change_24h_pct'])} 24h)")
    print(f"24h volume       : {s['total_volume_24h']:,.0f} {convert} ({_pct(s['volume_change_24h_pct'])} 24h)")
    print(f"BTC dominance    : {s['btc_dominance']:.2f}%")
    print(f"ETH dominance    : {s['eth_dominance']:.2f}%")
    print(f"Active coins     : {s['active_cryptocurrencies']:,}")
    print(f"Active exchanges : {s['active_exchanges']:,}")
    print(f"Last updated     : {s['last_updated']}")


if __name__ == "__main__":
    main()
