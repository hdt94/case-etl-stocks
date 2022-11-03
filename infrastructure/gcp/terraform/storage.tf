resource "google_storage_bucket" "results" {
  name     = "results-${var.PROJECT_ID}"
  location = var.REGION
}

resource "google_storage_bucket" "spark_jobs" {
  name     = "spark-jobs-${var.PROJECT_ID}"
  location = var.REGION
}

output "gs_results" {
  value = google_storage_bucket.results.url
}

output "gs_spark_jobs" {
  value = google_storage_bucket.spark_jobs.url
}
