sudo yum install docker

sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose

sudo chmod +x /usr/bin/docker-compose

sudo service docker start

sudo bash run.sh
