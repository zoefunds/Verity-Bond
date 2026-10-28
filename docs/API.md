# Contract API

The live Studionet contract is
`0xe6859D98D3cD2532A76684454fF2edA809cd4834`.

## Write methods

### `begin_identity(domain: str) -> str`

Creates a wallet- and domain-specific challenge. Returns JSON containing the
normalized domain, `/.well-known/veritybond.json` path, and challenge.

### `verify_identity(domain: str) -> str`

Fetches the well-known JSON document and verifies that its `wallet` equals the
caller and its `challenge` equals the stored challenge.

### `open_pact(...) -> str` (payable)

Parameters, in order:

1. `pact_id: str` — unique identifier, at most 64 characters.
2. `domain: str` — a currently verified publisher domain.
3. `origin_url: str` — HTTPS URL beneath that exact domain.
4. `statement: str` — normalized commitment of 30–500 characters.
5. `beneficiary: str` — address distinct from the publisher.
6. `term_days: int` — 14–1,095 days.

The attached value is the stake and must be at least one base unit. Opening a
pact fetches and semantically validates the origin baseline.

### `submit_evidence_round(pact_id, round_id, evidence_json) -> str`

Submits exactly two archive claims as a JSON array. Each item contains `source`,
`target_url`, `locator`, and the decoded body `digest`. Returns the admitted
round verdict.

### `challenge(pact_id: str) -> str` (payable)

Allows only the publisher to challenge a pact in `REVIEW` before its deadline.
The attached bond must equal `max(1, stake // 10)`.

### `beneficiary_release(pact_id: str) -> str`

Allows only the beneficiary to release a live pact after at least one admitted
`HOLDS` round. Returns the stake to the publisher and terminates the pact as
`RELEASED`.

### `finalize(pact_id: str) -> str`

Permissionlessly executes a terminal transition after the applicable pact,
review, or challenge deadline.

## View methods

- `get_pact(pact_id) -> dict` returns pact identity, timing, evidence summary,
  state, and accounting fields.
- `list_pacts() -> list` returns all pacts in creation order.
- `pact_evidence(pact_id) -> list` returns admitted evidence for one pact.
- `get_ledger() -> dict` returns total input, output, locked value, and pact
  count.
- `get_limits() -> dict` returns the contract's principal protocol limits.

## CLI examples

```sh
ADDRESS=0xe6859D98D3cD2532A76684454fF2edA809cd4834
RPC=https://studio.genlayer.com/api

genlayer schema "$ADDRESS" --rpc "$RPC"
genlayer call "$ADDRESS" get_limits --rpc "$RPC"
genlayer call "$ADDRESS" list_pacts --rpc "$RPC"
```

Write calls require an active, funded, unlocked GenLayer account. Consult the
installed CLI's `genlayer write --help` for its current value and fee flags.

