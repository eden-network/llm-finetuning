resource "google_bigquery_dataset" "llm" {
  dataset_id  = var.dataset_id
  description = var.dataset_description
  location    = var.location
}

resource "google_bigquery_table" "input_outputs" {
  dataset_id = var.dataset_id
  table_id   = var.table_id  
  schema     = file("${path.module}/input_outputs.json")
}

resource "google_bigquery_table" "stats" {
  dataset_id = var.dataset_id
  table_id   = var.stats_view_id
  view {
    query = templatefile("${path.module}/stats.sql", {
      project_id    = var.project_id,
      dataset_id    = var.dataset_id,
      view_id       = var.stats_view_id
    })
    use_legacy_sql = false
  }
}