# MenuTruth — Project Explorer draft

Status: prepared for review; finish authorized direct dashboard signing tests before describing all features as fully verified.

## Identity

Project name: MenuTruth

Suggested primary category: choose the closest available consumer/business application category in the live submission form. Suggested topics if available: Food & Hospitality; AI Verification. These labels are suggestions, not a claim about current form options.

Logo source: `dist/logo.svg`. A PNG export is included as `docs/menutruth-logo.png` when present.

Website: https://menutruth.mohamedansaf222.chatgpt.site

Repository: https://github.com/haris4587/MenuTruth

## Short summary

MenuTruth helps restaurant teams catch misleading menu claims after ingredient substitutions. Approved recipes, current ingredients and supplier declarations are locked into a GenLayer contract. Independent AI validator review checks description, dietary and disclosure consistency, then records the agreed finding and staff response in a verifiable ledger.

## Problem & product

Recipe substitutions often reach the kitchen before menu copy or front-of-house disclosures are updated. A dairy-for-oat-cream swap can leave a vegan claim on a menu. MenuTruth gives chefs and managers a shared change register with immutable baselines, attributed evidence, explicit uncertainty, three separate review checks and an acknowledgement history that preserves the original result.

## Why GenLayer

The central state transition requires semantic reasoning over ingredient statements and claims. The Intelligent Contract uses a constrained AI review, schema and quote checks, and `gl.vm.run_nondet_unsafe` with independent validator reassessment. Validators compare per-check statuses and the deterministic verdict. Without agreed review, no result is committed. A conventional server cannot unilaterally replace that consensus step.

## Reviewer walkthrough

1. Open the public website and jump to Kitchen ledger.
2. Open Garden tomato soup’s approved evidence: vegan menu wording and oat cream recipe.
3. Open Change #1: the fictional supplier declaration and current recipe introduce dairy cream (milk).
4. Inspect the three ISSUE findings and ACTION_REQUIRED verdict with exact excerpts.
5. Read the manager’s recorded proposed correction. The original verdict remains unchanged.
6. Follow the contract and transaction links. Compare with `evidence/live-verification.json`.
7. Inspect the source and run the local test suite. For writes, use the deploying manager in Studio or an explicitly authorized disposable chef account.

## Verified chain evidence

Network: GenLayer Studionet, 61999, https://studio.genlayer.com/api

Contract: https://explorer-studio.genlayer.com/address/0x9Bb33b418E0ab1472421f1e9749Aab4131DB784E

- Deployment: https://explorer-studio.genlayer.com/transactions/0x818f667b9468f87866446005f9028942295f814ea9d3da5bfa03cd6e3cef4235
- Register: https://explorer-studio.genlayer.com/transactions/0xb1d501c3c8571fd5b734b95930e63f5798a97006a7c3aed648ef6001fd597621
- Substitute: https://explorer-studio.genlayer.com/transactions/0xfe1055971818aa15670552b970832029665dd59fb78fe8e35b20759bd24600e4
- Staff address fix upgrade: https://explorer-studio.genlayer.com/transactions/0x3eda40e9676516297c2e524fd4edb05d02c2b32ef3a4aaec5b351de69e5fa146
- AI review: https://explorer-studio.genlayer.com/transactions/0x28c8ec7e5db636359f7c5a77c0c7c42359544b89b00d55ca052414f16c2fd9ed
- Acknowledge: https://explorer-studio.genlayer.com/transactions/0x0fbfada543730a9f6c29458d9317c72cec1cb596548cee4f66940bc01e90f27e

## Honest scope

This is a working hosted development sandbox demonstration, not mainnet food-safety infrastructure. Restaurant/supplier evidence is self-attested. No physical ingredient verification, cross-contact certification, laboratory testing, legal compliance determination, real restaurant adoption, or automated supplier-authenticity checks are claimed. No social posts or videos have been published on the user’s behalf.

Potential next development: supplier-signed evidence, bounded commit-pinned document retrieval, jurisdiction-specific review policies, corrections linked across recipe versions and multi-location restaurant workspaces.

## Supporting visuals

- Logo PNG: [menutruth-logo.png](menutruth-logo.png), 512×512.
- [Live home screenshot](screenshot-home.jpg).
- [Live ledger screenshot](screenshot-ledger.jpg).
- [Review evidence screenshot](screenshot-review.jpg).
- [Passing CI run](https://github.com/haris4587/MenuTruth/actions/runs/41433948499).
