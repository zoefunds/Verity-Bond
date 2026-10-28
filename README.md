# VerityBond

VerityBond is a standalone GenLayer intelligent contract for identity-bound,
evidence-diverse public commitment assurance. A publisher locks a stake behind
a public statement, independent web archives supply evidence, and deterministic
state transitions release or pay the escrow.

## Contract

The deployable contract is `contracts/VerityBond.py`. Its publisher identity
proof is served from `/.well-known/veritybond.json` and is scoped to the caller's
wallet and domain.

## Test

Run the direct deployment and lifecycle suite with:

```sh
gltest tests/direct -q
```

The suite covers deployment, identity challenge generation, baseline admission,
evidence quorum, replay resistance, archive digest validation, review and
challenge paths, beneficiary release, expiry behavior, and value conservation.

