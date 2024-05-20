variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "dataset_id" {
  description = "The BigQuery dataset ID."
  type        = string
}

variable "table_id" {
  description = "The ID of the BigQuery table for finalised data."
  type        = string
}

variable "stats_view_id" {
  description = "The ID of the BigQuery view for llm tokenization stats"
  type        = string
}