#!/bin/bash

# This script spins up a uvicorn server, #
# killing the last instance if running   #
# Have fun !				 #

public_address=`curl ifconfig.me`
port='8000'
startpage='docs'
parent_dir='unite-backend'
app_dir='unite-engine'

source '/home/ubuntu/fastapi-mysql/bin/activate'

pkill uvicorn
pkill python

echo Unite App Running available in http://$public_address:$port/$startpage 
uvicorn_args="--app-dir \"/home/ubuntu/$parent_dir/$app_dir\" app:app --reload --host 0.0.0.0 --port $port"
echo running with: uvicorn $uvicorn_args
uvicorn $uvicorn_args

