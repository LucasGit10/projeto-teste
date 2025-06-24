variable "project" {}
variable "region" {
  default = "us-central1"
}
variable "zone" {
  default = "us-central1-a"
}
variable "machine_type" {
  default = "e2-medium"
}
variable "credentials_file" {
  description = "Caminho do JSON de credenciais"
}
variable "public_key_path" {
  description = "Caminho da chave pública SSH"
}
