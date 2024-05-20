provider "google" {
  project = var.project_id
  region  = "us-central1"
}

locals {
  project_id               = var.project_id  
  location                 = "us-central1"
  dataset_id               = "llm"
  table_id                 = "input_outputs"
  stats_view_id            = "stats"    
}

module "bigquery" {
  source                   = "../../modules/bigquery"  
  project_id               = local.project_id  
  dataset_id               = local.dataset_id  
  table_id                 = local.table_id
  stats_view_id            = local.stats_view_id    
  location                 = local.location
}

output "dataset_id" {
  value = module.bigquery.dataset_id
}

output "table_id" {
  value = module.bigquery.table_id
}

output "stats_view_id" {
  value = module.bigquery.stats_view_id
}