# AWS Free-Tier Module (Optional)

This Terraform module is **optional** and not required for local runs. It exists so you can practice IaC with a tiny, free-tier-safe footprint.

## What it creates

- **S3 bucket** for incident exports
- **DynamoDB table** for runbook results (on-demand billing)
- **IAM role + policy** so an external system could read/write those resources

Everything here fits inside AWS free-tier usage when used responsibly.

## Files

- `main.tf` – All resource definitions
- `variables.tf` – Inputs you can customize
- `outputs.tf` – What Terraform will show you after apply

## How to use (if you want cloud practice)

```
cd infrastructure/aws-free-tier
terraform init
terraform apply
```

## Inputs you can change

- `aws_region` – default `us-east-1`
- `project_name` – used as a prefix for resource names
- `environment` – label for dev/stage/prod

## Free-tier notes

- S3 and DynamoDB have generous free-tier quotas.
- Costs can occur if you exceed free-tier limits.
- Always monitor your AWS billing dashboard.

## Why this is separated

ForgeOps Lab is local-first. This module is isolated so that:
- Local runs never touch the cloud
- Cloud experiments are opt-in only
- You can delete this folder without affecting the project
