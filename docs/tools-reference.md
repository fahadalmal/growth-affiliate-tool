# Tools reference

Eleven MCP tools, all read-only. Every tool that takes a time period uses the same
[`periodType` codes](period-type.md).

| #  | Tool                                                              | Purpose                          |
| -- | ----------------------------------------------------------------- | -------------------------------- |
| 1  | [`okx-affiliate-performance-summary`](#1-performance-summary)     | Aggregate metrics                |
| 2  | [`okx-affiliate-invitee-list`](#2-invitee-list)                   | Paginated invitee list           |
| 3  | [`okx-affiliate-invitee-detail`](#3-invitee-detail)               | Single invitee deep dive          |
| 4  | [`okx-affiliate-link-list`](#4-link-list)                         | Your invite links                |
| 5  | [`okx-affiliate-sub-affiliate-list`](#5-sub-affiliate-list)       | Sub-affiliates in MLRS network   |
| 6  | [`okx-affiliate-co-inviter-list`](#6-co-inviter-list)             | Channels where you co-invite     |
| 7  | [`affiliate_tvb_get_performance_summary`](#7-tvb-performance-summary) | TVB (Trading Volume Bonus) summary |
| 8  | [`affiliate_tvb_get_tier_breakdown`](#8-tvb-tier-breakdown)       | TVB bonus by fee tier            |
| 9  | [`affiliate_tvb_get_invitee_list`](#9-tvb-invitee-list)          | Paginated TVB invitee list       |
| 10 | [`affiliate_tvb_get_invitee_detail`](#10-tvb-invitee-detail)     | Single TVB invitee deep dive     |
| 11 | [`affiliate_tvb_get_link_list`](#11-tvb-link-list)               | TVB performance per link         |

> **Naming note:** All numeric values in the schema (page, limit, periodType, etc.) are passed
> as **strings**, not integers. Pass `"1"`, not `1`.

---

## 1. Performance summary

**Tool name:** `okx-affiliate-performance-summary`

Aggregate performance for the connected affiliate over a chosen time window.

### Parameters

| Param        | Type   | Required | Default  | Description                                                                       |
| ------------ | ------ | :------: | :------: | --------------------------------------------------------------------------------- |
| `periodType` | string | No       | `total`  | Time window — see [`period-type.md`](period-type.md). Omit for custom range.       |
| `begin`      | string | When custom | —      | Custom-range start, **Unix milliseconds**, inclusive. Required with `end`.         |
| `end`        | string | When custom | —      | Custom-range end, **Unix milliseconds**, inclusive. Required with `begin`.         |

> Pass `begin` and `end` for a custom range and omit `periodType` (or set any non-listed
> string). The server treats unknown `periodType` values as "use the supplied date range".

### Return shape

```json
{
  "msg": "",
  "code": "0",
  "data": [{
    "depAmt": "37337746.56",
    "inviteeCnt": "1885",
    "uTime": "1778222037000",
    "details": [
      {"commissionCategory": "SPOT",       "commission": "27327.74", "vol": "174375947.61", "traderCnt": "574", "firstTraderCnt": "574"},
      {"commissionCategory": "DERIVATIVE", "commission": "497463.39", "vol": "...",         "traderCnt": "785", "firstTraderCnt": "785"},
      {"commissionCategory": "BSC",        "commission": "4.18",      "vol": "1305.16",     "traderCnt": "2",   "firstTraderCnt": "2"}
    ]
  }]
}
```

### Field map (response)

| Field                            | Meaning                                                       |
| -------------------------------- | ------------------------------------------------------------- |
| `depAmt`                         | Total deposits in window                                      |
| `inviteeCnt`                     | Invitee count                                                 |
| `uTime`                          | Server snapshot time, Unix ms                                  |
| `details[]`                      | Per-category breakdown (SPOT / DERIVATIVE / BSC)              |
| `details[].commissionCategory`   | `"SPOT"` / `"DERIVATIVE"` / `"BSC"`                            |
| `details[].commission`           | Commission earned in that category                             |
| `details[].vol`                  | Trading volume in that category                                |
| `details[].traderCnt`            | Active traders in that category                                |
| `details[].firstTraderCnt`       | First-time traders in that category                            |

> **No top-level `commission` total** — sum across `details[]` to get the grand total.

---

## 2. Invitee list

**Tool name:** `okx-affiliate-invitee-list`

Paginated list of your direct invitees with their trading, deposit, and KYC stats.

### Parameters

| Param                | Type   | Required | Default | Description                                                                                  |
| -------------------- | ------ | :------: | :-----: | -------------------------------------------------------------------------------------------- |
| `page`               | string | No       | `"1"`   | Page number (starts at 1). Non-numeric values fall back to `"1"`.                            |
| `limit`              | string | No       | `"10"`  | Items per page. **Practical max is `"95"`** — see [FAQ](faq.md) on the `limit ≥ 99 → 500` bug. |
| `periodType`         | string | No       | `total` | Time window for stat fields                                                                   |
| `begin`              | string | When custom | —    | Custom-range start, Unix ms                                                                   |
| `end`                | string | When custom | —    | Custom-range end, Unix ms                                                                     |
| `commissionCategory` | string | No       | —       | Filter by category — `SPOT` / `DERIVATIVE` / `BSC`                                            |
| `kycStatus`          | string | No       | —       | `verified` (KYC2+) / `unverified`                                                             |
| `keyword`            | string | No       | —       | Substring match on UID or channel name                                                       |
| `subAffiliateUid`    | string | No       | —       | Filter to invitees attributed to a specific sub-affiliate UID                                |
| `orderBy`            | string | No       | `cTime` | Sort field — `cTime` (join time) / `depAmt` / `vol` / `fee` / `rebate`                        |
| `orderDir`           | string | No       | `desc`  | Sort order — `asc` / `desc`                                                                   |

### Return shape (each row)

```json
{
  "uid": "...",
  "channelName": "CRYPTO1818",
  "country": "CN",
  "kycStatus": "verified",
  "kycTime": "1755440968000",
  "joinTime": "1755424349000",
  "firstTradeTime": "1755496800000",
  "feeTierRank": "6",
  "rebateRate": "0.2000",
  "isCompliant": true,
  "depAmt": "10329631.36",
  "totalCommission": "104146.07",
  "totalFee": "347153.57",
  "totalVol": "1186843492.29"
}
```

`depAmt`, `totalCommission`, `totalFee`, `totalVol` are **scoped to the requested
`periodType`**. To get lifetime totals, omit `periodType` (default is `total`).

> **No `total` count in the response** — keep paginating until you get an empty `data` array.
> See [FAQ](faq.md) for pagination strategy.

---

## 3. Invitee detail

**Tool name:** `okx-affiliate-invitee-detail`

Deep dive on a single invitee, by external UID.

### Parameters

| Param | Type   | Required | Description                                  |
| ----- | ------ | :------: | -------------------------------------------- |
| `uid` | string | ✅       | The invitee's external UID (from list above) |

### Return fields

```json
{
  "uid": "743072917935893796",
  "affiliateCode": "CRYPTO1818",
  "region": "China",
  "level": "Lv1",
  "inviteeLevel": "2",
  "inviteeRebateRate": "0.2",
  "joinTime": "1755424349000",
  "kycTime": "1755440968744",
  "firstTradeTime": "1755496800000",
  "depAmt": "10329631.35",
  "wdAmt": "9795977.54",
  "totalVol": "1186843492.29",
  "totalCommission": "104146.07",
  "accFee": "347153.56",
  "volMonth": "37.04"
}
```

`volMonth` is the calendar-month-to-date trading volume — useful for spotting users whose
activity dropped this month even though their lifetime numbers look healthy.

> ⚠️ Passing a UID that does not exist or is not your invitee returns
> `code: 51621, msg: "The user isn't your invitee"` rather than a 404 — see
> [FAQ](faq.md#q-invitee-detail-returns-the-user-isnt-your-invitee).

---

## 4. Link list

**Tool name:** `okx-affiliate-link-list`

Your invite links with cumulative invitee count, trader count, and commission.

### Parameters

| Param        | Type   | Required | Default  | Description                                                  |
| ------------ | ------ | :------: | :------: | ------------------------------------------------------------ |
| `page`       | string | No       | `"1"`    | Page number                                                   |
| `limit`      | string | No       | `"10"`   | Items per page; max `"95"` in practice                       |
| `linkType`   | string | No       | —        | `standard` (your own invite links) / `co_inviter` (links you co-invite on) |
| `linkStatus` | string | No       | —        | `normal` / `abnormal`                                         |

> ⚠️ **Invalid `linkType` / `linkStatus` values are silently accepted** and the filter is
> dropped (you get all rows back). Always check returned `linkType` / `linkStatus` matches
> what you asked for. See [FAQ](faq.md#q-i-passed-linktypewhatever-and-still-got-all-results).

### Return fields (per link)

```json
{
  "channelId": "49323294",
  "channelName": "CRYPTO1818",
  "joinLink": "https://okx.com/join/CRYPTO1818",
  "linkType": "standard",
  "linkStatus": "normal",
  "isDefault": true,
  "cTime": "1705316204000",
  "inviterCommissionRate": "0.3000",
  "coInviterCommissionRate": "0.0000",
  "inviteeDiscountRate": "0.2000",
  "inviteeCnt": "1850",
  "traderCnt": "830",
  "totalCommission": "524194.29",
  "commission24h": "173.09"
}
```

`commission24h` is the rolling 24-hour commission for that specific link — handy for spotting
which channels are hot right now.

---

## 5. Sub-affiliate list

**Tool name:** `okx-affiliate-sub-affiliate-list`

Sub-affiliates in your MLRS (multi-level referral system) network. **Lifetime data only** —
the new schema removed the per-period filter.

### Parameters

| Param                | Type   | Required | Default | Description                                                          |
| -------------------- | ------ | :------: | :-----: | -------------------------------------------------------------------- |
| `page`               | string | No       | `"1"`   | Page number                                                          |
| `limit`              | string | No       | `"10"`  | Items per page; max `"95"` in practice                                |
| `commissionCategory` | string | No       | —       | `SPOT` / `DERIVATIVE` / `BSC`                                         |
| `keyword`            | string | No       | —       | Search by sub-affiliate UID                                           |
| `orderBy`            | string | No       | (joinTime newest first) | `cTime` / `depAmt` / `vol` / `fee` / `rebate`         |
| `orderDir`           | string | No       | `desc`  | `asc` / `desc`                                                        |

### Return fields (per row)

Sub-affiliate UID, invitee count, trader count, trading volume, fees, commission. Lifetime
only.

---

## 6. Co-inviter list

**Tool name:** `okx-affiliate-co-inviter-list`

Channels where you are listed as a co-inviter (i.e. you share commission on those links).

### Parameters

| Param        | Type   | Required | Default | Description                          |
| ------------ | ------ | :------: | :-----: | ------------------------------------ |
| `page`       | string | No       | `"1"`   | Page number                          |
| `limit`      | string | No       | `"10"`  | Items per page; max `"95"` in practice |
| `linkStatus` | string | No       | —       | `normal` / `abnormal`                 |

### Return fields (per row)

Channel name, your commission share, partner / co-inviter UIDs, invitee stats, channel
status. The schema is rich (~22 fields per row).

---

## 7. TVB performance summary

**Tool name:** `affiliate_tvb_get_performance_summary`

Aggregate **TVB (Trading Volume Bonus)** performance for the connected affiliate over a chosen
time window. Unlike the commission-based tools above, TVB is a bonus program **settled in
USDC**: the affiliate earns a `multiplier`-scaled bonus on eligible trading volume from valid
invitees. Returns a single summary object inside a one-element `data` array.

> ℹ️ **Availability & cadence:** TVB is currently offered in **select regions only** —
> affiliates outside supported regions get all-zero results (not an error). The bonus
> **accrues hourly** and settles in **USDC**, so figures can lag real activity by up to ~1h;
> `uTime` marks the last hourly update.

### Parameters

| Param        | Type   | Required     | Default | Description                                                                                                                                            |
| ------------ | ------ | :----------: | :-----: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `periodType` | string | No           | `total` | Stats window — one of `last_7d`, `last_30d`, `this_month`, `last_month`, `this_week`, `today`, `total`, `custom`. When omitted: falls back to `custom` if both `begin` and `end` are present, otherwise `total`. |
| `begin`      | string | When `custom` | —      | Custom-range start, **Unix milliseconds**, inclusive. Required with `end`. Ignored unless `periodType=custom`.                                          |
| `end`        | string | When `custom` | —      | Custom-range end, **Unix milliseconds**, inclusive. Required with `begin`. Ignored unless `periodType=custom`.                                          |

> ⚠️ Unlike the other tools, TVB summary exposes `custom` as an **explicit** `periodType`
> value, and the custom window (`end - begin`) **must not exceed 90 days**.

### Return shape

```json
{
  "code": "0",
  "msg": "",
  "data": [{
    "tradingVolBonus": "12500.00",
    "validVol": "8450000.00",
    "eligibleVol": "8200000.00",
    "validInviteeCnt": "342",
    "validTraderCnt": "198",
    "eligibleTraderCnt": "176",
    "validDepAmt": "1250000.00",
    "validFirstTraderCnt": "54",
    "validFirstDepositorCnt": "61",
    "multiplier": "0.5",
    "ccy": "USDC",
    "uTime": "1784192118000"
  }]
}
```

### Field map (response)

| Field                       | Meaning                                                                          |
| --------------------------- | -------------------------------------------------------------------------------- |
| `data[]`                    | One-element array containing the summary object                                  |
| `tradingVolBonus`           | Accrued trading volume bonus in the window (USDC)                                 |
| `validVol`                  | Valid trading volume in the window (USDC)                                         |
| `eligibleVol`               | Eligible trading volume feeding the bonus, in the window (USDC)                   |
| `validInviteeCnt`           | Valid invitees (dedup count)                                                      |
| `validTraderCnt`            | Valid traders (dedup count)                                                       |
| `eligibleTraderCnt`         | Eligible traders — traded and earned bonus (dedup count)                          |
| `validDepAmt`               | Deposit from valid invitees in the window (USDC)                                  |
| `validFirstTraderCnt`       | Valid first-time traders / FTT (dedup count)                                      |
| `validFirstDepositorCnt`    | Valid first-time depositors / FTD (dedup count)                                   |
| `multiplier`                | Affiliate's bonus multiplier as a decimal ratio (e.g. `"0.5"` = 50%)             |
| `ccy`                       | Settlement currency. Constant `"USDC"`                                            |
| `uTime`                     | Last **hourly** data-update timestamp, Unix ms (`""` when the table has no partition yet) |

> All numeric values are returned as **decimal strings** — parse with `Decimal` / `BigDecimal`
> to preserve precision.

---

## 8. TVB tier breakdown

**Tool name:** `affiliate_tvb_get_tier_breakdown`

Decompose the affiliate's total **TVB (Trading Volume Bonus)** across the invitee's trading
**fee tier** for a chosen window. Returns a single object inside a one-element `data` array:
the affiliate-level total plus a `tiers` array, one row per fee tier. TVB is not available to
invitees at VIP 6 or above, so the breakdown **caps at VIP 5**.

> ℹ️ Same availability & cadence as the TVB summary: **select regions only** (out-of-region
> affiliates get all-zero results), **hourly** accrual, settled in **USDC**.

### Parameters

| Param        | Type   | Required     | Default | Description                                                                                                                                            |
| ------------ | ------ | :----------: | :-----: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `periodType` | string | No           | `total` | Stats window — `last_7d`, `last_30d`, `this_month`, `last_month`, `this_week`, `today`, `total`, `custom`. When omitted: falls back to `custom` if both `begin` and `end` are present, otherwise `total`. |
| `begin`      | string | When `custom` | —      | Custom-range start, **Unix milliseconds**, inclusive. Required with `end`. Ignored unless `periodType=custom`.                                          |
| `end`        | string | When `custom` | —      | Custom-range end, **Unix milliseconds**, inclusive. Required with `begin`. Ignored unless `periodType=custom`.                                          |

> ⚠️ The custom window (`end - begin`) **must be between 1 and 90 days**, and `begin` **must
> not be earlier than 180 days ago** — data is retained for the past 180 days only.
> `multiplier`, `ccy` and `uTime` are **not** window-scoped.

### Return shape

```json
{
  "code": "0",
  "msg": "",
  "data": [{
    "multiplier": "0.5",
    "tradingVolBonus": "15.5875",
    "ccy": "USDC",
    "uTime": "1784505600000",
    "tiers": [
      { "level": "Regular User", "validVol": "82000", "eligibleVol": "60000", "bonusRate": "0.00035",  "tradingVolBonus": "10.5"   },
      { "level": "VIP 1",        "validVol": "21500", "eligibleVol": "20000", "bonusRate": "0.000305", "tradingVolBonus": "3.05"   },
      { "level": "VIP 5",        "validVol": "1300",  "eligibleVol": "1000",  "bonusRate": "0.000155", "tradingVolBonus": "0.0775" }
    ]
  }]
}
```

### Field map (response)

| Field                 | Meaning                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| `multiplier`          | Affiliate's bonus multiplier as a decimal ratio (e.g. `"0.5"` = 50%). Not window-scoped |
| `tradingVolBonus`     | Affiliate-level accrued bonus in the window (USDC). Equals the sum of `tiers[].tradingVolBonus` |
| `ccy`                 | Settlement currency. Constant `"USDC"`                                           |
| `uTime`               | Last hourly data-update timestamp, Unix ms (`""` when no data yet)               |
| `tiers[]`             | One row per invitee fee tier (Regular User + VIP 1–VIP 5)                        |
| `tiers[].level`       | Tier display label — `"Regular User"`, `"VIP 1"` … `"VIP 5"`                     |
| `tiers[].validVol`    | Valid trading volume for this tier in the window (USDC)                          |
| `tiers[].eligibleVol` | Eligible (bonus-generating) volume for this tier in the window (USDC)            |
| `tiers[].bonusRate`   | Programme's fixed bonus rate for this tier, as a decimal (e.g. `"0.00035"`)      |
| `tiers[].tradingVolBonus` | Bonus accrued from this tier's `eligibleVol`, with `multiplier` applied (USDC) |

---

## 9. TVB invitee list

**Tool name:** `affiliate_tvb_get_invitee_list`

Paginated list of the affiliate's **TVB** invitees plus affiliate-level aggregates for a
window. Returns `totalPage` at the top level and a single object in `data` holding the
aggregates and an `invitees` array of per-row records.

> ⚠️ **A UID may appear in more than one row.** Each row is a **fee-tier segment** — `level`
> and its amounts are scoped to that segment. Do **not** treat repeated UIDs as duplicates.

> ℹ️ The window scopes the metric fields by activity time; it does **not** change which
> invitees are returned (that is driven by `feeTier` / `keyword`). Aggregates cover the whole
> filtered result set and are constant across pages.

### Parameters

| Param        | Type            | Required     | Default    | Description                                                                                             |
| ------------ | --------------- | :----------: | :--------: | ------------------------------------------------------------------------------------------------------- |
| `periodType` | string          | No           | `total`    | Stats window — the eight [`periodType` codes](period-type.md). Scopes metric fields only.               |
| `begin`      | string          | When `custom` | —         | Custom-range start, **Unix ms**, inclusive. Required with `end`.                                        |
| `end`        | string          | When `custom` | —         | Custom-range end, **Unix ms**, inclusive. Required with `begin`.                                        |
| `feeTier`    | array of string | No           | —          | Filter by fee-tier **code(s)**: `"0"` = Regular, `"10"`–`"18"` = VIP1–VIP9. Numeric codes only — **not** the display name in the response `level` field. |
| `tradeType`  | string          | No           | `ALL`      | Product for the volume metrics: `ALL`, `SPOT`, `DERIVATIVE`, `BSC`. Selects which amounts to read, not which invitees. |
| `keyword`    | string          | No           | —          | Search invitees by UID.                                                                                 |
| `orderBy`    | string          | No           | `joinTime` | Sort field: `joinTime`, `validDepAmt`, `validVol`.                                                      |
| `orderDir`   | string          | No           | `desc`     | Sort order: `asc`, `desc`.                                                                              |
| `page`       | string          | No           | `1`        | 1-indexed page number. Non-numeric falls back to 1.                                                     |
| `limit`      | string          | No           | `100`      | Items per page, clamped to `[1, 100]`.                                                                   |

> ⚠️ Custom-window rules match the summary tool: `end - begin` **1–90 days**, `begin` no
> earlier than **180 days ago**.

### Return shape

```json
{
  "code": "0",
  "msg": "",
  "totalPage": "1",
  "data": [{
    "tradingVolBonus": "18.75",
    "validVol": "60700.00",
    "eligibleVol": "47400.00",
    "validDepAmt": "2246.56",
    "validInviteeCnt": "3",
    "validFirstTraderCnt": "1",
    "validTraderCnt": "2",
    "eligibleTraderCnt": "1",
    "invitees": [{
      "uid": "855082962927686909",
      "joinTime": "1782129625000",
      "country": "NL",
      "kycTime": "1782129625324",
      "affiliateCode": "54022003",
      "firstTradeTime": "1782216025000",
      "level": "Regular User",
      "validVol": "12500.00",
      "eligibleVol": "9800.00",
      "validDepAmt": "106.56",
      "note": "VIP client from IG"
    }]
  }]
}
```

### Field map (response)

| Field                            | Meaning                                                                       |
| -------------------------------- | ----------------------------------------------------------------------------- |
| `totalPage`                      | Total page count under the current filters & page size (**same level as `data`**) |
| `data[].tradingVolBonus`         | Accrued TVB bonus in the window (USDC)                                         |
| `data[].validVol` / `eligibleVol`| Valid / eligible trading volume in the window (USDC)                           |
| `data[].validDepAmt`             | Deposit from valid invitees in the window (USDC)                              |
| `data[].validInviteeCnt`         | Distinct valid invitees                                                        |
| `data[].validFirstTraderCnt`     | Distinct valid first-time traders / FTT                                        |
| `data[].validTraderCnt`          | Distinct valid invitees who traded                                             |
| `data[].eligibleTraderCnt`       | Distinct traders who traded and generated bonus                                |
| `data[].invitees[]`              | Result rows — **the same `uid` may repeat, scoped to a fee-tier segment**      |
| `invitees[].uid`                 | Invitee UID                                                                    |
| `invitees[].joinTime` / `kycTime` / `firstTradeTime` | Unix ms (`""` when not verified / not traded)              |
| `invitees[].country`             | Country / region                                                               |
| `invitees[].affiliateCode`       | Invite code the invitee registered via                                         |
| `invitees[].level`               | Fee-tier **display name** (e.g. `"VIP 1"`) — not the numeric `feeTier` filter code |
| `invitees[].validVol` / `eligibleVol` | Trading / eligible volume in the window (USDC)                            |
| `invitees[].validDepAmt`         | Invitee's deposit in the window (USDC). `""` when masked (no deposit-view permission) |
| `invitees[].note`                | Affiliate's private note on the invitee. `""` when none                        |

> No per-invitee bonus is exposed — bonus is surfaced only at the affiliate-total (§7) and
> per-fee-tier (§8) level.

---

## 10. TVB invitee detail

**Tool name:** `affiliate_tvb_get_invitee_detail`

A single **TVB** invitee's profile looked up by UID — identity, direct inviter, KYC, fee tier,
and **lifetime** trading / eligible volume and deposit. Returns a single object inside a
one-element `data` array. There are **no time-window parameters**.

### Parameters

| Param | Type   | Required | Description        |
| ----- | ------ | :------: | ------------------ |
| `uid` | string | **Yes**  | The invitee's UID. |

### Return shape

```json
{
  "code": "0",
  "msg": "",
  "data": [{
    "uid": "855082962927686909",
    "inviterUid": "853364004059009741",
    "joinTime": "1782129625000",
    "country": "NL",
    "kycStatus": "verified",
    "kycTime": "1782129625324",
    "affiliateCode": "54022003",
    "note": "VIP client from IG",
    "firstTradeTime": "",
    "level": "Regular User",
    "validVol": "12500.00",
    "eligibleVol": "9800.00",
    "validDepAmt": "1420.11"
  }]
}
```

### Field map (response)

| Field           | Meaning                                                                             |
| --------------- | ----------------------------------------------------------------------------------- |
| `uid`           | Invitee UID                                                                          |
| `inviterUid`    | Public UID of the direct inviter (the affiliate itself for a direct invitee; a sub-affiliate's UID under MLRS). `""` when unresolvable |
| `joinTime`      | Invite-relationship establishment time, Unix ms                                     |
| `country`       | Country / region                                                                     |
| `kycStatus`     | `"verified"` / `"unverified"`                                                         |
| `kycTime`       | KYC time, Unix ms; `""` when not verified                                            |
| `affiliateCode` | Invite code the invitee registered via                                               |
| `note`          | Affiliate's private note. `""` when none                                             |
| `firstTradeTime`| First trade time, Unix ms; `""` when not traded                                      |
| `level`         | Fee-tier display name (`"Regular User"`, `"VIP 1"`–`"VIP 9"`)                        |
| `validVol` / `eligibleVol` | Lifetime trading / eligible volume (USDC)                                 |
| `validDepAmt`   | Lifetime deposit (USDC). `""` when masked (no deposit-view permission)               |

> An invalid or unresolvable `uid` returns HTTP 200 with a non-zero business code and empty
> `data` — it does not reveal whether the UID exists. No per-invitee bonus is exposed.

---

## 11. TVB link list

**Tool name:** `affiliate_tvb_get_link_list`

Paginated list of the affiliate's **TVB** invite links, each row carrying that link's TVB
performance for a window. Returns `totalPage` at the top level and a `data` array with one
element per link.

### Parameters

| Param        | Type   | Required     | Default | Description                                                              |
| ------------ | ------ | :----------: | :-----: | ------------------------------------------------------------------------ |
| `periodType` | string | No           | `total` | Stats window — the eight [`periodType` codes](period-type.md).           |
| `begin`      | string | When `custom` | —      | Custom-range start, **Unix ms**, inclusive. Required with `end`.         |
| `end`        | string | When `custom` | —      | Custom-range end, **Unix ms**, inclusive. Required with `begin`.         |
| `page`       | string | No           | `1`     | 1-indexed page number. Non-numeric falls back to 1.                      |
| `limit`      | string | No           | `100`   | Items per page, clamped to `[1, 100]`.                                    |
| `linkType`   | string | No           | —       | Link kind filter: `standard` (invite link) or `co_inviter`. Omit for all. |
| `linkStatus` | string | No           | —       | Link status filter: `normal` or `abnormal`. Omit for all.                |

> ⚠️ Custom-window rules match the summary tool: `end - begin` **1–90 days**, `begin` no
> earlier than **180 days ago**.

### Return shape

```json
{
  "code": "0",
  "msg": "",
  "totalPage": "3",
  "data": [{
    "channelId": "245012001",
    "channelName": "Summer Campaign",
    "linkStatus": "normal",
    "joinLink": "https://www.okx.com/join/245012001",
    "note": "IG bio link",
    "validInviteeCnt": "58",
    "validTraderCnt": "24",
    "eligibleTraderCnt": "21",
    "validVol": "96500.00",
    "eligibleVol": "84200.00",
    "tradingVolBonus": "12.63",
    "cTime": "1782129625000"
  }]
}
```

### Field map (per link)

| Field               | Meaning                                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| `totalPage`         | Total page count = `ceil(total / limit)` (**same level as `data`**)            |
| `channelId`         | The link's channel ID                                                          |
| `channelName`       | Link display name                                                              |
| `linkStatus`        | `"normal"` / `"abnormal"`                                                       |
| `joinLink`          | Shareable invite URL                                                           |
| `note`              | User-defined note on the link. `""` when none                                  |
| `validInviteeCnt`   | Distinct valid invitees attributed to this link (`"0"` when none)              |
| `validTraderCnt`    | Distinct valid traders on this link (`"0"` when none)                          |
| `eligibleTraderCnt` | Distinct eligible (bonus-generating) traders (`"0"` when none)                 |
| `validVol` / `eligibleVol` | Valid / eligible trading volume on this link (USDC; `"0"` when none)     |
| `tradingVolBonus`   | Accrued TVB bonus from this link (USDC; `"0"` when none)                        |
| `cTime`             | Link creation time, Unix ms. `""` when unavailable                             |

---

## Notes shared across all tools

- **All numeric inputs are passed as strings.** `page`, `limit`, `begin`, `end` — all
  strings.
- **Numeric outputs are decimal strings** — preserve precision when parsing (parse as
  `Decimal` / `BigDecimal`).
- **Timestamps are Unix epoch milliseconds** — `joinTime`, `firstTradeTime`, `kycTime`,
  `uTime`, `cTime`.
- **Token lifetime is approximately 1 hour.** Most clients refresh transparently; if you see
  401s, trigger your client's MCP reconnect / refresh.
- **Rate limit:** the endpoint returns `429 Too Many Requests` (`code: 50011`) for bursty
  traffic. Aim for ≤ 5 RPS; back off on 429.
- **`limit` cap:** schema says max 100 but anything ≥ 99 currently returns `500 system
  error`. Use `≤ 95` to be safe.
