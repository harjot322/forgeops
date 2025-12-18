output "incident_exports_bucket" {
  value = aws_s3_bucket.incident_exports.bucket
}

output "runbook_results_table" {
  value = aws_dynamodb_table.runbook_results.name
}

output "forgeops_role_arn" {
  value = aws_iam_role.forgeops_role.arn
}
