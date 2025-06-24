provider "google" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials_file)
}

resource "google_compute_instance" "vm_instance" {
  name         = "app-instance"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}  # cria IP externo
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.public_key_path)}"
  }

  tags = ["http-server", "https-server"]
}
