terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "3.1.1"
    }
  }
}

provider "null" {}

resource "null_resource" "local_vm" {
  provisioner "local-exec" {
    command = "echo 'Ambiente local pronto'"
  }
}

output "instance_ip" {
  value = "127.0.0.1"
}
