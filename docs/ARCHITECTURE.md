# Architecture

## Purpose

VerityBond turns a public statement into a time-bounded, staked pact. The
contract admits a baseline, monitors independent archive captures, and applies
deterministic payout rules to the resulting evidence verdicts.

The intelligent layer answers one question: whether the exact commitment
`HOLDS`, is `WEAKENED`, is `ABSENT`, or is `INDETERMINATE` in admitted content.
It cannot select recipients, amounts, deadlines, or state transitions.

## Participants

- **Publisher:** proves control of a web domain, publishes the commitment, and
  escrows the stake.
- **Beneficiary:** receives the stake after an unchallenged or confirmed breach
  and may release a positively monitored pact.
- **Evidence submitter:** permissionlessly submits an approved two-source
  archive round.
- **Validators:** fetch evidence and reach consensus on web results and semantic
  findings.

## State machine

```text
LIVE ── two consecutive breach rounds ──> REVIEW
LIVE ── term elapsed ───────────────────> RELEASED or REFUNDED
LIVE ── beneficiary release ────────────> RELEASED
REVIEW ── publisher bond ───────────────> CHALLENGED
REVIEW ── review deadline ──────────────> PAID
CHALLENGED ── holding quorum ───────────> RELEASED
CHALLENGED ── breach quorum ────────────> PAID
CHALLENGED ── deadline/uncertainty ─────> PAID
```

At normal expiry, `RELEASED` requires intact evidence coverage, at least two
monitoring rounds, a final `HOLDS` verdict, and evidence freshness through the
term. Otherwise the publisher receives a `REFUNDED` result. Both are terminal,
but the state distinguishes successful monitoring from a non-punitive return.

## Evidence admission

Each round requires exactly two different approved adapters:

1. Internet Archive Wayback Machine (`WAYBACK`)
2. Arquivo.pt (`ARQUIVO_PT`)

For each claim the contract checks the adapter-specific locator, exact target
URL, 14-digit capture timestamp, archive metadata, decoded SHA-256 content
digest, archive SHA-1 wire digest, pact term, chronological ordering, and replay
key. A conclusive round requires both adapters to agree.

## Current limits

| Limit | Value |
| --- | ---: |
| Minimum stake | 1 base unit |
| Pact term | 14–1,095 days |
| Evidence quorum | 2 sources |
| Consecutive breach rounds | 2 |
| Maximum indeterminate rounds | 3 |
| Identity validity | 2,592,000 seconds (30 days) |
| Review window | 604,800 seconds (7 days) |
| Challenge window | 604,800 seconds (7 days) |
| Maximum coverage gap | 604,800 seconds (7 days) |
| Minimum release rounds | 2 |
| Maximum evidence body | 180,000 bytes/characters after decoding |
| Maximum statement | 500 characters |

## Value conservation

`total_in` increases only when a pact stake or challenge bond enters.
`total_out` increases on terminal transfers. `get_ledger()` exposes both values
and `currently_locked = total_in - total_out`. Every tested terminal path moves
the full stake and, when present, the full challenge bond.

