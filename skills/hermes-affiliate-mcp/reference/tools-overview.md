# OKX Affiliate MCP tools — quick reference

After install, Hermes Agent exposes these seven tools. The first six share the
`okx-affiliate-` prefix (omitted below; actual names are
`mcp_okx_affiliate_okx_affiliate_<tool>`); the TVB tool has its own name (see the footnote):

| Tool                              | What it returns                                                       |
| --------------------------------- | --------------------------------------------------------------------- |
| `performance-summary`             | Aggregate metrics — invitees, deposits, volume, commission, broken down by Spot / Derivatives / BSC over a chosen window |
| `invitee-list`                    | Paginated invitee list with deposits, trading, KYC status             |
| `invitee-detail`                  | Deep dive on a single invitee by external UID                          |
| `link-list`                       | Your invite links + commission rates + cumulative stats (incl. 24h)   |
| `sub-affiliate-list`              | Sub-affiliates in your MLRS network (lifetime data)                   |
| `co-inviter-list`                 | Channels where you are listed as a co-inviter                          |
| `affiliate_tvb_get_performance_summary` †  | TVB (Trading Volume Bonus) aggregate summary — accrued bonus, valid/eligible volume, valid invitee/trader counts, FTT/FTD, `multiplier`; settled in USDC |

† Full canonical name (does **not** follow the `okx-affiliate-*` prefix convention); exposed
by Hermes as `mcp_okx_affiliate_affiliate_tvb_get_performance_summary`.

Full parameter and field reference: see the upstream docs at
<https://github.com/okx/growth-affiliate-tool/blob/master/docs/tools-reference.md>.

## Natural-language prompts (examples)

- "What was my affiliate performance yesterday?"
- "Show me my top 20 invitees by 7-day commission."
- "List all invite links with their 24-hour commission."
- "Who in my network qualifies for VIP1 upgrade?"
- "Which whales in my top-50 LTV have gone inactive in the last 30 days?"

Hermes will route these to the right tool automatically.
