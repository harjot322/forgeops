variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "forgeops"
}

variable "environment" {
  description = "Environment label"
  type        = string
  default     = "dev"
}
