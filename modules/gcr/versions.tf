# Example configuration of terraform providers

terraform {
  required_version = "~> 1.10.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.44.0"
    }
  }
}