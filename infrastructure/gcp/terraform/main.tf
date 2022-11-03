terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.41.0"
    }

    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.41.0"
    }
  }
}

provider "google" {
  project = var.PROJECT_ID
  region  = var.REGION
}

provider "google-beta" {
  project = var.PROJECT_ID
  region  = var.REGION
}

resource "google_project_service" "composer" {
  disable_on_destroy = false
  project            = data.google_project.project.project_id
  service            = "composer.googleapis.com"
}

resource "google_project_service" "compute" {
  disable_on_destroy = false
  project            = data.google_project.project.project_id
  service            = "compute.googleapis.com"
}

resource "google_project_service" "dataproc" {
  disable_on_destroy = false
  project            = data.google_project.project.project_id
  service            = "dataproc.googleapis.com"
}

data "google_project" "project" {
  project_id = var.PROJECT_ID
}

data google_compute_default_service_account default {
  depends_on = [google_project_service.compute]
}
