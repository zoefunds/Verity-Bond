# Live Studionet E2E Report

## Result

**PASS — 4/4 live checks passed at 2026-10-28 08:53:48 UTC.**

This report records read-only tests executed against the real GenLayer
Studionet RPC at `https://studio.genlayer.com/api`. It is separate from the 22
direct-VM tests, which use deterministic local web and model mocks.

## Target

| Field | Observed value |
| --- | --- |
| Contract | `VerityBond` |
| Address | `0xe6859D98D3cD2532A76684454fF2edA809cd4834` |
| Chain ID | `61999` |
| Deployment transaction | `0xf8431603750fc671114065506c0399f6b2727fac6decb6bc04e8b40988b9e4d0` |
| Deployer | `0x7401c129EDfc26E68FE19309fE461eb3Db1058Eb` |
| Transaction status | `FINALIZED` |
| Consensus result | `MAJORITY_AGREE` |
| Consensus rounds | 1 |
| Validator votes | 3 `AGREE`, 2 `IDLE` after quorum |
| Created at | `2026-10-28T08:44:06.225650+00:00` |

The leader and three agreeing executions reported `SUCCESS`. The two idle
validators were cancelled after quorum, with
`CONSENSUS_VALIDATOR_QUORUM_REACHED`; they are not failed contract executions.

## Checks

### 1. Deployed source integrity — PASS

`genlayer code` returned source identical to
`contracts/VerityBond.py`. The normalized deployed source SHA-256 is:

```text
8666fb1294c9bc106863b15788f94e81f0d12881852a704102d1c16fc4b7524d
```

### 2. Public schema — PASS

The live schema exposed all 12 expected public methods:

- Writes: `begin_identity`, `verify_identity`, `open_pact`,
  `submit_evidence_round`, `challenge`, `beneficiary_release`, `finalize`
- Views: `get_pact`, `list_pacts`, `pact_evidence`, `get_ledger`, `get_limits`

The live schema also marked `open_pact` and `challenge` payable and marked all
five view methods read-only.

### 3. Protocol limits — PASS

| Limit | Live value |
| --- | ---: |
| Evidence quorum | 2 |
| Consecutive breach rounds | 2 |
| Maximum indeterminate rounds | 3 |
| Identity TTL | 2,592,000 seconds |
| Review window | 604,800 seconds |
| Maximum coverage gap | 604,800 seconds |
| Minimum release rounds | 2 |
| Maximum body size | 180,000 |

These values match the reviewed repository source.

### 4. Ledger and state — PASS

The real `get_ledger` response was:

```json
{
  "currently_locked": "0",
  "pacts": "0",
  "total_in": "0",
  "total_out": "0"
}
```

The conservation invariant holds: `currently_locked = total_in - total_out`.
`list_pacts` also remains empty at the time of this test.

## Reproduce

The live test is opt-in so ordinary local test runs do not depend on network
availability:

```sh
RUN_STUDIONET_E2E=1 python3 -m pytest tests/e2e/test_studionet.py -v
```

The test requires the GenLayer CLI and network access. It performs only
read-only calls and does not require a private key.

The deterministic suite remains:

```sh
gltest tests/direct -q
```

## Scope

This live E2E proves deployment finality, deployed-source identity, ABI/schema
availability, protocol-limit consistency, and live ledger conservation. The
full identity, archive, semantic-classification, challenge, and payout paths are
covered by the 22 direct-VM lifecycle tests. A destructive live lifecycle was
not created because it would require publishing a controlled domain proof and
permanent archive captures for a new funded pact.
