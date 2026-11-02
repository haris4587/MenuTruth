# Evidence policy and sources

MenuTruth evaluates consistency within restaurant-provided declarations. The contract does not authenticate a supplier label, observe food preparation, identify hidden contamination or give medical advice.

Policy v1 is embedded in the contract, hashed and copied to every dish at registration. Evidence is committed on-chain at registration/submission. The same committed record is available independently to each validator; no validator relies only on the leader’s opinion. Exact matching applies to status decisions, while explanation wording can differ. Invalid schemas or ungrounded quotes fail closed. An undecided transaction leaves the submitted record available for a future retry; the app does not label it successful.

Reference sources consulted on 2026-11-02:

- FDA: https://www.fda.gov/food/buy-store-serve-safe-food/food-allergies-what-you-need-know — reference vocabulary for milk, eggs, fish, crustacean shellfish, tree nuts, peanuts, wheat, soybeans and sesame.
- FDA: https://www.fda.gov/food/nutrition-education-resources-materials/gluten-and-food-labeling — gluten-free claims require more than reading a recipe; the rule includes a less-than-20-ppm condition and other criteria.
- FDA: https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies — many unpackaged restaurant foods fall outside the packaged-food labeling requirements discussed on this page. MenuTruth does not generalize those requirements to every restaurant or jurisdiction.
- GenLayer: https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle — independent validator review and stable decision-field comparison.
- GenLayer: https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio — hosted Studio networks and development environment.
- GenLayer: https://docs.genlayer.com/api-references/genlayer-js — SDK contract and transaction actions. Stable installed SDK is pinned to 1.1.8; the development preview requires separately matched tooling and is not used here.

Future evidence integrations should accept immutable supplier documents with independent authenticity checks, content hashes and bounded retrieval, record provenance, and provide policies scoped to a restaurant’s jurisdiction. Live mutable data is deliberately not fetched in this first version because the review concerns locked internal recipe declarations rather than current market facts.
