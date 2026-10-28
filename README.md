# VerityBond

VerityBond is a standalone GenLayer intelligent contract for identity-bound,
evidence-diverse public commitment assurance. A publisher locks a stake behind
a public statement, independent web archives supply evidence, and deterministic
state transitions release or pay the escrow.

## Live deployment

| Field | Value |
| --- | --- |
| Network | GenLayer Studionet |
| Chain ID | `61999` |
| Contract | `0xe6859D98D3cD2532A76684454fF2edA809cd4834` |
| Transaction | `0xf8431603750fc671114065506c0399f6b2727fac6decb6bc04e8b40988b9e4d0` |
| Deployer | `0x7401c129EDfc26E68FE19309fE461eb3Db1058Eb` |
| Status | Finalized (`MAJORITY_AGREE`) |
| Deployed | 2026-10-28 08:44:06 UTC |

Post-deployment verification retrieved the public schema and called
`get_ledger`. A real identity-bound E2E pact now leaves the live ledger at one
pact, one unit in, zero out, and one locked as of 2026-10-28 09:05:01 UTC.
Machine-readable deployment data is in
[`deployments/studionet.json`](deployments/studionet.json).

## Repository

- Deployable contract: [`contracts/VerityBond.py`](contracts/VerityBond.py)
- Direct deployment and lifecycle tests: [`tests/direct`](tests/direct)
- Architecture and lifecycle: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Public contract API: [`docs/API.md`](docs/API.md)
- Deployment and verification: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- Security properties and assumptions: [`docs/SECURITY.md`](docs/SECURITY.md)
- Test coverage: [`docs/TESTING.md`](docs/TESTING.md)
- Live Studionet E2E evidence: [`docs/E2E_REPORT.md`](docs/E2E_REPORT.md)

## Quick verification

Requirements are Python 3, the GenLayer CLI, and `gltest`.

```sh
gltest tests/direct -q
genlayer call 0xe6859D98D3cD2532A76684454fF2edA809cd4834 get_ledger \
  --rpc https://studio.genlayer.com/api
```

The current direct suite contains 22 tests. It covers deployment, identity
challenge generation, baseline admission, evidence quorum, replay resistance,
archive digest validation, review and challenge paths, beneficiary release,
expiry behavior, and value conservation.

Run the five live Studionet state-verification checks with:

```sh
RUN_STUDIONET_E2E=1 python3 -m pytest tests/e2e/test_studionet.py -v
```

The persisted state comes from real `begin_identity`, `verify_identity`, and
payable `open_pact` transactions. See [`docs/E2E_REPORT.md`](docs/E2E_REPORT.md)
for transaction hashes, observed state, and the remaining terminal-settlement
boundary.

## Identity proof

Before opening a pact, a publisher calls `begin_identity(domain)` and publishes
the returned challenge at `https://<domain>/.well-known/veritybond.json`:

```json
{
  "wallet": "0x...",
  "challenge": "..."
}
```

The publisher then calls `verify_identity(domain)`. The proof is wallet- and
domain-bound and remains valid for 30 days.

## Important

Studionet is a development network. The deployment is not a production security
or economic guarantee. Review the documented assumptions before using real
value.

