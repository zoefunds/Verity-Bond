# Deployment

## Current Studionet release

| Field | Value |
| --- | --- |
| Contract | `VerityBond` |
| Source | `contracts/VerityBond.py` |
| Source SHA-256 | `8666fb1294c9bc106863b15788f94e81f0d12881852a704102d1c16fc4b7524d` |
| Source commit | `425950978521db00486a1c4995c94375e82377ef` |
| Network | Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Address | `0xe6859D98D3cD2532A76684454fF2edA809cd4834` |
| Transaction | `0xf8431603750fc671114065506c0399f6b2727fac6decb6bc04e8b40988b9e4d0` |
| Current status | `FINALIZED` |
| Consensus result | `MAJORITY_AGREE` |
| Consensus rounds | 1 |
| Deployed at | 2026-10-28 08:44:06 UTC |
| Last live verification | 2026-10-28 08:56:48 UTC |

The address and transaction are also recorded in
`deployments/studionet.json`.

`ACCEPTED` was the deployment receipt status returned immediately after
consensus. The transaction has since advanced to its terminal `FINALIZED`
status; documentation and deployment metadata now report the current state.

## Reproduce a deployment

1. Install and configure the GenLayer CLI.
2. Select Studionet and an intentionally funded deployment account.
3. Run the direct test suite.
4. Deploy the contract.
5. Verify the schema and initial ledger.

```sh
genlayer network set studionet
gltest tests/direct -q
genlayer deploy --contract contracts/VerityBond.py \
  --rpc https://studio.genlayer.com/api

genlayer schema <contract-address> \
  --rpc https://studio.genlayer.com/api
genlayer call <contract-address> get_ledger \
  --rpc https://studio.genlayer.com/api
```

Expected initial ledger:

```json
{
  "currently_locked": "0",
  "pacts": "0",
  "total_in": "0",
  "total_out": "0"
}
```

Never commit a private key, keystore password, `.env` file, or unlocked
credential. Lock the deployment account after use.

