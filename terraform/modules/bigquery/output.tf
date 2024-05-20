output "dataset_id" {
  description = "The dataset ID for housing things relatede to local llms"
  value = google_bigquery_dataset.llm.dataset_id
}

output "table_id" {
  description = "The ID of the input_outputs table created."
  value       = google_bigquery_table.input_outputs.table_id
}

output "stats_view_id" {
  description = "The ID of the stats view created."
  value       = google_bigquery_table.stats.table_id
}