#!/bin/bash

# This script spins up a uvicorn server, #
# killing the last instance if running   #
# Have fun !				 #

public_address=`curl ifconfig.me`
port='8000'
startpage='docs'
parent_dir='unite-backend'
app_dir='unite-engine'
full_app_path="$HOME/$parent_dir/$app_dir"
environment_args="$HOME/fastapi-mysql/bin/activate"


pkill uvicorn
pkill python

echo "starting env with: source $environment_args"
source $environment_args

echo "Unite App Running available in http://$public_address:$port/$startpage"
echo starting $app_dir with: nohup uvicorn --app-dir $full_app_path app:app --reload --host 0.0.0.0 --port $port \> $HOME/unite.log
nohup uvicorn --app-dir $full_app_path app:app --reload --host 0.0.0.0 --port $port > $HOME/unite.log

