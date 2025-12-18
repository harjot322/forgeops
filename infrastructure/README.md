# Infrastructure

This folder contains infrastructure-as-code (IaC). It is **optional** and not required for local runs.

## Why it exists

ForgeOps Lab is local-first, but some learners want a tiny cloud footprint to practice IaC. The subfolder here provides a minimal AWS free-tier module that can be applied safely in a personal account.

## Folder guide

- `aws-free-tier/` – Terraform module to create a basic, free-tier-safe setup.

If you do not want any cloud usage, you can ignore this folder completely.
