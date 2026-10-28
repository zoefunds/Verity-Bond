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

## Studionet deployment

- Contract address: `0xe6859D98D3cD2532A76684454fF2edA809cd4834`
- Deployment transaction: `0xf8431603750fc671114065506c0399f6b2727fac6decb6bc04e8b40988b9e4d0`
- Deployer: `0x7401c129EDfc26E68FE19309fE461eb3Db1058Eb`
- Network: GenLayer Studionet (`61999`)

The deployment was verified by reading its public schema and calling
`get_ledger`, which returned an empty, conserved ledger.

