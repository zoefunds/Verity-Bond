# Security

## Enforced properties

- Identity challenges bind the caller's wallet and normalized domain.
- Origin URLs must use HTTPS beneath the verified domain.
- Identity proofs expire after 30 days.
- Baselines must contain a holding commitment before stake admission.
- Evidence requires two unique, approved archive adapters.
- Archive locators, metadata, timestamps, target URLs, decoded content hashes,
  and archive wire digests are checked before classification.
- Round IDs and individual captures are replay-protected.
- Evidence must advance chronologically and remain inside the pact term.
- Negative findings require an excerpt present in the admitted body.
- The intelligent classifier cannot choose recipients or transfer amounts.
- No administrator or oracle key can cancel a pact or move escrow.
- Deadline finalization is permissionless, preventing indefinite fund freezes.
- Challenge bonds are included in terminal accounting.

## Trust assumptions

- GenLayer validator consensus and configured model providers operate according
  to the network protocol.
- Wayback Machine and Arquivo.pt metadata accurately identify their captures.
- HTTPS and DNS correctly route the publisher's identity and origin URLs.
- The GenLayer runtime implements address, transfer, storage, and nondeterminism
  primitives as documented.

## Operational risks

- Archive coverage can be absent, delayed, or incomplete. Uncertainty is
  bounded but cannot manufacture missing evidence.
- Semantic classification can be ambiguous. Two-source agreement and grounded
  excerpts reduce, but do not eliminate, model risk.
- A seven-day maximum evidence gap requires regular monitoring for a successful
  release outcome.
- Studionet is a development environment and should not custody production
  value.
- Anyone possessing a deployment or publisher private key controls that wallet.
  Use dedicated accounts and do not reuse exposed or throwaway keys.

## Reporting

When reporting a vulnerability, include the affected method, preconditions,
minimal reproduction, expected behavior, observed behavior, and potential value
impact. Do not exploit a live pact or publish private keys.

