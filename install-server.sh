# this is supposed to be run on a fresh ubuntu machine
apt-get install -y unzip screen
wget https://minecraft.azureedge.net/bin-linux/bedrock-server-1.19.2.02.zip
unzip bedrock-server-1.19.2.02.zip -d server
ufw allow 19132/tcp