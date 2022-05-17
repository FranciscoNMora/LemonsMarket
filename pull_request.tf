# Configure and downloading plugins for aws
provider "aws" {
  region     = "${var.aws_region}"
}

# Creating EC2 Instance
resource "aws_instance" "demoinstance" {
  # AMI based on region
  ami = "${lookup(var.ami, var.aws_region)}"

  # Launching instance into subnet
  subnet_id = "subnet-0f3d270f5092600ca"

  # Instance type
  instance_type = "${var.instancetype}"

  # Count of instance
  count= "${var.master_count}"

  # SSH key that we have generated above for connection
  key_name = "terraform-test"

  # Attaching security group to our instance
  vpc_security_group_ids = ["sg-0c426aa05dc1e705f"]

  # Attaching Tag to Instance
  tags = {
    Name = "Example-${var.PR}"
  }

  # Root Block Storage
  root_block_device {
    volume_size = "40"
    volume_type = "standard"
  }

  #EBS Block Storage
  ebs_block_device {
    device_name = "/dev/sdb"
    volume_size = "80"
    volume_type = "standard"
    delete_on_termination = false
  }

  # SSH into instance
  connection {

    # Host name
    host = self.public_ip
    # The default username for our AMI
    user = "ec2-user"
    # Private key for connection
    private_key = "${var.AWS_EC2_PEM}"
    # Type of connection
    type = "ssh"
  }

  # Installing splunk on newly created instance
  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install docker -y",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "sudo chkconfig docker on",
      "sudo yum install -y git",
      "sudo chmod 666 /var/run/docker.sock",
      "sudo curl -L https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "git clone https://github.com/FranciscoNMora/LemonsMarket.git",
      "cd LemonsMarket",
      "git checkout ${var.HASH}",
      "docker-compose up -d"
  ]
 }
}

  output "server_id1" {
    value = "${aws_instance.demoinstance[0].public_ip}"
  }

