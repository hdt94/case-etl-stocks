resource "google_service_account_iam_member" "custom_service_account" {
  depends_on = [google_project_service.composer]

  service_account_id = data.google_compute_default_service_account.default.name
  role = "roles/composer.ServiceAgentV2Ext"
  member   = "serviceAccount:service-${data.google_project.project.number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_composer_environment" "demo_env" {
  provider = google-beta
  name     = "demo-env"
  region = var.REGION

  config {
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    software_config {
      image_version = "composer-2.0.29-airflow-2.3"
    }
  }
}

output composer_env {
  value = {
    location = google_composer_environment.demo_env.region
    name = google_composer_environment.demo_env.name
  }
}
