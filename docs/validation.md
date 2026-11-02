# Validation record

This document separates local logic checks, hosted GenVM execution and browser checks.

## Passed

- `npm test`: 18 Python tests using a minimal GenLayer host test double; these exercise actual contract functions, but do not substitute for GenVM validation. 13 JS lifecycle tests exercise the status classifier.
- `npm run build`: pinned `genlayer-js` and esbuild bundle compiled successfully.
- Studio schema extraction and deployment of actual Python source.
- Full consensus Studio-signed registration, substitution submission, semantic review, acknowledgement, and a Studio sandbox upgrade fixing checksum-normalization for staff permission lookup.
- SDK reads confirmed contract identity, baseline and review evidence; review outcome ACTION_REQUIRED with all three ISSUE checks.
- Desktop browser inspected the rendered design and live data, filled example forms, and created a temporary account without exposing its key.

## Pending

Automatic approval review rejected the planned grant of chef permission to `0x8c6d54f1ad093Ad0d0a1BE364b344ddd66cf41A0` on `0x9Bb33b418E0ab1472421f1e9749Aab4131DB784E`. It also rejected the signed negative-path test from that unprivileged account. Neither transaction was submitted. No workaround was used.

The direct dashboard signing path must be tested after explicit authorization: grant temporary staff via the Studio manager, submit a harmless demo substitution from the dashboard, verify successful receipt and state, exercise a bounded failed call, revoke the staff role and disconnect. The ephemeral account may need replacement if the browser session ends; never silently substitute a new recipient.

The Studio handoff and receipt tracker provide the built-in-account workflow without exporting Studio keys. Optional session signing does not automatically connect to Studio’s local account store.

## Reproduce

Run `npm ci`, `npm test`, `npm run build`, then `node scripts/verify-live.mjs`. The latter makes read-only calls and records actual current state and transaction receipts; hosted Studio can reset, so a later failure must be reported rather than silently replacing addresses or evidence.

The Studio upgrade operation has FINALIZED status without a leader execution receipt. The verifier separately compares the currently deployed source with the repository source. Other five operations have successful leader receipts. The SDK may include cancelled validator receipts in `leader_receipt`; the lifecycle classifier selects the actual leader and has a regression test for cancellation after quorum.
