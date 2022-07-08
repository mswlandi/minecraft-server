# minecraft-server
scripts to run a Bedrock Server and an automatic backup system for the world, on a fresh remote ubuntu machine

## steps to install
- clone this repo with `git clone https://github.com/mswlandi/minecraft-server`
- run `cd minecraft-server`
- run install-server.sh

## run server on background
- run `screen -S server`
- run run-server.sh
- exit the screen session with `CTRL + A, D` (to go back run `screen -r`)

## backup the world
- run install-auto-backup.sh
- in your own computer, complete the Authentication section in https://pythonhosted.org/PyDrive/quickstart.html to get the client_secrets.json
- create a folder in your google drive called minecraft-backups
- get your client_secrets.json and credentials.json in the remote computer somehow lol (you can create the files there and manually input it, it's just one line for both), in the same folder as backup.py

## load a backup world into the server
- run install-auto-backup.sh if you haven't already
- stop the server
- inside the world's folder, change the name of the world in the file levelname.txt to `Bedrock level` if it isn't already
- rename the world's folder name to `Bedrock level`
- compress it to a file named `Bedrock level.zip`
- upload it to the minecraft-backups drive folder
- assuming you have the client_secrets.json (instructions in the last section), run load-backup.py
- run the server again