# Testing

## Run the suite

```sh
gltest tests/direct -q
```

Current result: **22 passed** on 2026-10-28.

## Coverage

The direct GenLayer VM suite verifies:

- empty deployment state and protocol limits;
- wallet/domain challenge scoping and the VerityBond well-known path;
- rejection of unverified publishers;
- baseline admission and grounded semantic excerpts;
- successful multi-round coverage and expiry release;
- indeterminate-round behavior and refunds;
- consecutive breach escalation to review;
- successful, failed, and expired challenge paths;
- correct division of stake and challenge bond;
- archive timestamp, metadata, and digest integrity;
- separation of wire SHA-1 and decoded-content SHA-256 digests;
- evidence and round replay resistance;
- beneficiary-only positive release;
- failure of a single early round or coverage gap to qualify for release;
- conservation of value across terminal paths; and
- the current GenLayer response and transfer interfaces.

## Live smoke verification

The deployed contract was checked with:

```sh
genlayer schema 0xe6859D98D3cD2532A76684454fF2edA809cd4834 \
  --rpc https://studio.genlayer.com/api
genlayer call 0xe6859D98D3cD2532A76684454fF2edA809cd4834 get_ledger \
  --rpc https://studio.genlayer.com/api
```

The schema exposed all documented methods. The latest ledger check at
2026-10-28 08:48:04 UTC was empty and conserved.

