# this is supposed to be run on a fresh ubuntu machine
apt-get install -y unzip screen
wget https://minecraft.azureedge.net/bin-linux/bedrock-server-1.19.10.03.zip
unzip bedrock-server-1.19.10.03.zip -d server
ufw allow 19132/tcp