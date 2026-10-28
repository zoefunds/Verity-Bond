# Live Studionet E2E Report

## Result

**PASS — real identity, HTTPS verification, baseline admission, and payable
pact creation executed on Studionet. The resulting 5/5 live state checks passed
at 2026-10-28 09:05:01 UTC.**

This report records both real write transactions and subsequent state checks
against the GenLayer Studionet RPC at `https://studio.genlayer.com/api`. It is
separate from the 22 direct-VM tests, which use deterministic local web and
model mocks.

## Real write lifecycle executed

| Step | Transaction | Result |
| --- | --- | --- |
| `begin_identity` | `0xcc06f8428ab896793c3788b456503f2c51cc80afbbee6369f377d0646f239331` | `MAJORITY_AGREE` |
| `verify_identity` | `0xbd34aad73463f6a45a5e98965d2077a78fa7655c73150bf1cbe9d6a3f9cc6392` | `MAJORITY_AGREE`; validators returned `ok=true` |
| `open_pact` with value `1` | `0x41b926060d537957ef742fdfad6c36464847f11b1804efae47fc02d85e07276e` | `MAJORITY_AGREE`; returned `pact opened with identity-bound publisher` |

The identity proof was served from
`https://veritybond-live-e2e.vercel.app/.well-known/veritybond.json`. The
baseline was fetched from
`https://veritybond-live-e2e.vercel.app/commitment`. This exercised real HTTPS
fetching, validator nondeterministic consensus, identity storage, semantic
baseline classification, value transfer into the contract, pact storage, and
read-back from the deployed contract.

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

### 4. Ledger conservation — PASS

The real `get_ledger` response was:

```json
{
  "currently_locked": "1",
  "pacts": "1",
  "total_in": "1",
  "total_out": "0"
}
```

The conservation invariant holds: `currently_locked = total_in - total_out`.

### 5. Persisted real pact — PASS

| Field | Observed value |
| --- | --- |
| Pact ID | `VB-LIVE-E2E-20261028-01` |
| State | `LIVE` |
| Stake | `1` |
| Publisher | `0x7401c129EDfc26E68FE19309fE461eb3Db1058Eb` |
| Beneficiary | `0xe2743b213418428A5BfBc7D9dDb8ec7c4c0D36De` |
| Created | `2026-10-28T09:03:42.358812Z` |
| Expires | `2026-11-11T09:03:42Z` |
| Baseline digest | `a4f65d22be3a7afe699a6e992b06fe5c106ebea4ba7250239aae32b9da168f2e` |
| Statement digest | `725d3c3bc90aa06f0b96ea77e24a8dd81827ce72752b9bdae78ddb6d0da15565` |

`get_pact` and `list_pacts` both returned this pact from real contract storage.

## Explorer evidence

- [`begin_identity` transaction](https://explorer-studio.genlayer.com/tx/0xcc06f8428ab896793c3788b456503f2c51cc80afbbee6369f377d0646f239331)
- [`verify_identity` transaction](https://explorer-studio.genlayer.com/tx/0xbd34aad73463f6a45a5e98965d2077a78fa7655c73150bf1cbe9d6a3f9cc6392)
- [`open_pact` transaction](https://explorer-studio.genlayer.com/tx/0x41b926060d537957ef742fdfad6c36464847f11b1804efae47fc02d85e07276e)
- [Live contract](https://explorer-studio.genlayer.com/address/0xe6859D98D3cD2532A76684454fF2edA809cd4834)

## Archive progress

A real Wayback Save Page Now capture was requested at 2026-10-28 09:06:55
UTC under job `spn2-f1991b44e65c497763fb3babebf9a1805a19eb76`. It was not yet
visible in the CDX index at the immediate follow-up check. Arquivo.pt's capture
is also not yet available. The contract correctly refuses an evidence round
until both independent adapters expose post-creation captures with matching
metadata and digests.

## Reproduce

The live test is opt-in so ordinary local test runs do not depend on network
availability:

```sh
RUN_STUDIONET_E2E=1 python3 -m pytest tests/e2e/test_studionet.py -v
```

The repeatable test requires the GenLayer CLI and network access. It reads and
asserts the state created by the recorded write transactions and does not need
a private key for reruns.

The deterministic suite remains:

```sh
gltest tests/direct -q
```

## Scope

This live E2E now proves deployment finality, deployed-source identity,
ABI/schema availability, protocol-limit consistency, real identity challenge,
real public proof verification, real baseline classification, payable pact
creation, persisted pact state, and live ledger conservation.

It does **not yet claim terminal settlement**. The contract enforces a minimum
14-day term, and an early beneficiary release requires a post-creation evidence
round from both Wayback Machine and Arquivo.pt. Those independent archives can
take hours to expose new captures. Until that evidence exists or the pact term
ends, the truthful live state is `LIVE` with one unit locked. Terminal paths
remain covered by the 22 deterministic direct-VM lifecycle tests.
