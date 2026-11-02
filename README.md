# MenuTruth

**What’s on the menu. What’s in the dish. Keep them in sync.**

MenuTruth is a restaurant recipe-change ledger powered by a real GenLayer Intelligent Contract. It helps managers and chefs catch menu descriptions and dietary disclosures that became inconsistent after a substitution. It records the evidence, validator-agreed findings and staff response in a shared, verifiable history.

- Website: https://menutruth.mohamedansaf222.chatgpt.site
- Network: **GenLayer Studionet, chain ID 61999** (hosted development sandbox; not a mainnet deployment)
- Contract: [`0x9Bb33b418E0ab1472421f1e9749Aab4131DB784E`](https://explorer-studio.genlayer.com/address/0x9Bb33b418E0ab1472421f1e9749Aab4131DB784E)
- Source: [contracts/menutruth.py](contracts/menutruth.py)
- Machine-readable deployment: [dist/deployment.json](dist/deployment.json)
- Verification: [evidence/live-verification.json](evidence/live-verification.json)

## The trust problem

A chef substitutes dairy cream for oat cream. The menu still says “vegan,” and front-of-house staff still have the old ingredient list. A normal recipe spreadsheet can silently drift or be overwritten. MenuTruth preserves the original claims and the submitted recipe change, obtains independent semantic review through GenLayer consensus, and records an attributable staff response. The trusted object is the record and the agreed consistency finding, not the truth of an unobserved kitchen.

## How it works

1. The deploying manager registers a dish’s approved menu, complete recipe and disclosure. The fixed review policy and SHA-256 commitments are stored with the record.
2. The manager or an authorized chef submits a complete current recipe, supplier evidence and a change note. The approved baseline remains unchanged.
3. A staff member requests `review_change`. Inside `gl.vm.run_nondet_unsafe`, the leader runs a constrained AI review. Validators independently run the same task against the same on-chain evidence, check output schemas and verbatim excerpts, and compare all three status fields and the derived verdict.
4. The contract records **description**, **dietary**, and **disclosure** results. Any ISSUE produces ACTION_REQUIRED; otherwise any UNKNOWN produces INCONCLUSIVE; only all CONSISTENT yields CONSISTENT. A failure to obtain consensus does not commit a review.
5. The manager acknowledges the result with an action note. That preserves the verdict; it does not prove the action was performed. Corrected menus are registered as new baseline records.

GenLayer is central: a deterministic text search cannot reliably reason about compound ingredients, meaning-preserving substitutions or implied dietary claims. Validator consensus controls the semantic state transition. This is not a chatbot response saved by an arbitrary backend.

## Use the app

The public dashboard reads live contract state through `genlayer-js`. Browse the recipe book and change journal, inspect original evidence and exact review quotes, and filter records by status.

**Built-in Studio account workflow (used for the verified demonstration):**

1. Open [GenLayer Studio](https://studio.genlayer.com/run-debug). Load `contracts/menutruth.py` or import the deployed contract address. Use the original deploying account for manager operations.
2. Fill a form in MenuTruth while disconnected. The app prepares the exact contract address, method and arguments for Studio. Sign in Studio using **Normal (Full Consensus)** mode.
3. Paste the resulting transaction hash into MenuTruth’s Transaction desk. The app fetches its actual receipt, distinguishes pending / accepted / finalized / execution failure, and refreshes the live ledger after commitment. Hashes are retained locally for resumed tracking.

**Optional dashboard signing:** Create a temporary chef account in the account dialog. The manager must explicitly authorize that address using `set_chef`. The generated key stays in browser memory and disappears on reload. Advanced users may import an existing disposable test account for session-only signing. No MetaMask, backend signer, bundled private key or server-held wallet is used. Studio has no cross-origin account-sharing API; the app does not claim to connect automatically to Studio’s browser-local key store.

Only manager-authorized addresses can mutate this demonstration contract. Public visitors can inspect evidence and prepare Studio calls; creating a temporary account does not grant permissions. Do not enter confidential recipes: all contract evidence is public.

## Contract API

| Method | Role | Effect |
| --- | --- | --- |
| `register_dish(name, menu, recipe, disclosure)` | Manager | Append immutable approved baseline |
| `submit_change(dish_id, recipe, supplier_evidence, note)` | Manager / authorized chef | Append immutable substitution evidence |
| `review_change(change_id)` | Manager / authorized chef | Run independent semantic consensus once |
| `acknowledge(change_id, action)` | Manager | Append one staff response, retain verdict |
| `set_chef(address, allowed)` | Manager | Grant / revoke staff role |
| `get_info()` | Public | Identity, counts, manager, policy hash |
| `get_dish(dish_id)` / `get_change(change_id)` | Public | Full evidence and result as JSON text |
| `is_staff(address)` | Public | Role lookup |

Inputs have strict size limits. Reviews require exactly three ordered result objects, allowed statuses, bounded explanations, and evidence-grounded excerpts. Evidence is explicitly untrusted prompt material. Unknown evidence never becomes a food-safety certificate. Contract state uses GenLayer `TreeMap` records with monotonic IDs. The UI bounds routine loads to the newest 100 dishes and changes; older IDs remain queryable in Studio.

## Evidence quality & limitations

Restaurant recipe and supplier statements are **self-attested**, committed on-chain and attributed to submitting staff. No real supplier or restaurant is implied by the clearly labeled demonstration fixture. Exact quotes establish traceability to the submitted evidence, not authenticity of the supplier or physical preparation. The app does not scrape mutable web pages or treat a link as verified evidence.

The fixed advisory policy uses the FDA’s nine major allergen categories as a reference vocabulary, rather than asserting universal restaurant labeling obligations. Absence claims, missing compound ingredients and unknown cross-contact are treated conservatively. Gluten-free cannot be established solely from recipe text. See [docs/evidence-policy.md](docs/evidence-policy.md) for authoritative source links and scope.

Studionet is a hosted sandbox with simulated validators and resettable state. The address and transaction links are evidence of tested sandbox execution, not production security or permanence. Studio supports code upgrades; the case-normalization fix was applied and its upgrade receipt is retained. AI review remains fallible. Operational use needs authenticated supplier documents, jurisdiction-specific policies, access administration, kitchen controls and human review.

## Run locally

Requires Node.js 22+ and Python 3.12+ (the local logic suite uses only the standard library).

```sh
npm ci
npm test
npm run build
python -m http.server 8080 --directory dist
```

Open `http://localhost:8080`. No API keys or environment secrets are required for public reads. `dist/deployment.json` selects the verified deployment. Dependency versions and lockfile are committed; the browser SDK is bundled locally. `node scripts/verify-live.mjs` performs read-only verification of the demonstration state and its six finalized receipts.

## Validation status

- 18 Python contract-logic tests: permissions, input limits, immutable commitments, independent assessment calls, disagreement, output schema, exact quote grounding, conservative precedence, acknowledgement order and replay protection.
- 13 JavaScript lifecycle tests: pending and terminal statuses, numeric SDK statuses, receipt arrays and accepted execution failures.
- Live Studio: deployment, dish registration, substitution submission, code-fix upgrade, AI review and acknowledgement finalized successfully. The three checks flagged ISSUE and ACTION_REQUIRED remained after acknowledgement.
- Browser: live SDK reads, dashboard layout, example forms, temporary account creation, record inspection and Studio transaction tracking checked.
- **Pending authorization:** successful direct dashboard signing with an authorized temporary chef, and signed negative-path tests. Automated approval review blocked the temporary role grant and the attempted negative write before submission. No permission was granted to that test address. See [docs/validation.md](docs/validation.md).

Do not describe the final pending items as passed. The Studio-signed end-to-end workflow is verified; the optional direct dashboard write path still needs its authorized live test.

## Project Explorer

Submission copy, reviewer walkthrough and verified links are in [docs/project-explorer.md](docs/project-explorer.md). The project is not represented as fully submission-ready until the remaining authorized dashboard write checks pass.

## License

MIT. See [LICENSE](LICENSE).
