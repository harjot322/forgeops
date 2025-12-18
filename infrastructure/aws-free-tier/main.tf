terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "incident_exports" {
  bucket = "${var.project_name}-${var.environment}-incident-exports"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "runbook_results" {
  name         = "${var.project_name}-${var.environment}-runbook-results"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_iam_role" "forgeops_role" {
  name               = "${var.project_name}-${var.environment}-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_policy" "forgeops_policy" {
  name        = "${var.project_name}-${var.environment}-policy"
  description = "Access to incident exports and runbook results"

  policy = data.aws_iam_policy_document.forgeops.json
}

resource "aws_iam_role_policy_attachment" "forgeops_attach" {
  role       = aws_iam_role.forgeops_role.name
  policy_arn = aws_iam_policy.forgeops_policy.arn
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

data "aws_iam_policy_document" "forgeops" {
  statement {
    actions = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
    resources = [
      aws_s3_bucket.incident_exports.arn,
      "${aws_s3_bucket.incident_exports.arn}/*"
    ]
  }

  statement {
    actions   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Query"]
    resources = [aws_dynamodb_table.runbook_results.arn]
  }
}
