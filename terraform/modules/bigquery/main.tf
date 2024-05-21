resource "google_bigquery_dataset" "llm" {
  dataset_id  = var.dataset_id
  description = "Housing auxiliary data assoiciated with local llm finetuning"
  location    = var.location
}

resource "google_bigquery_table" "input_outputs" {
  dataset_id          = var.dataset_id
  table_id            = var.table_id
  schema              = file("${path.module}/input_output.json")
  depends_on          = [google_bigquery_dataset.llm]
  deletion_protection = false
}

resource "google_bigquery_table" "stats" {
  dataset_id = var.dataset_id
  table_id   = var.stats_view_id
  view {
    query = templatefile("${path.module}/stats.sql", {
      project_id = var.project_id,
      dataset_id = var.dataset_id,
      view_id    = var.table_id
    })
    use_legacy_sql = false
  }
  depends_on          = [google_bigquery_dataset.llm, google_bigquery_table.input_outputs]
  deletion_protection = false
}

resource "google_bigquery_table" "tokenizer_token_limit" {
  dataset_id = var.dataset_id
  table_id   = "tokenizer_token_limit"
  view {
    query = file("${path.module}/tokenizer_token_limit.sql")    
    use_legacy_sql = false
  }
  deletion_protection = false
}