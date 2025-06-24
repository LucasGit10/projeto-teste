variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "ssh_key_name" {
  description = "Nome da chave SSH criada na AWS"
}

variable "app_port" {
  description = "Porta exposta pela aplicação"
  default     = 8080
}
