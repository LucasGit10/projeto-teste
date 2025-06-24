variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "orquestrador-rg"
}

variable "vm_name" {
  default = "orquestrador-vm"
}

variable "admin_username" {
  default = "ubuntu"
}

variable "ssh_public_key" {
  description = "Caminho para a chave pública SSH"
}
