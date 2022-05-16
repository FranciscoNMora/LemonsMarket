
# Defining Private Key
variable "AWS_EC2_PEM" {
  type = string
}

# Definign Key Name for connection
variable "key_name" {
  default = "tests"
  description = "Desired name of AWS key pair"
}

# Defining Region
variable "aws_region" {
  default = "us-east-1"
}

# Defining AMI
variable "ami" {
  default = {
    eu-west-1 = "ami-0ea3405d2d2522162"
    us-east-1 = "ami-09d95fab7fff3776c"
  }
}

# Defining Instace Type
variable "instancetype" {
  default = "t2.medium"
}

# Defining Master count
variable "master_count" {
  default = 1
}

variable "HASH" {
  type = string
}

variable "GITHUB_REF" {
  type = string
}

