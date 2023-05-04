#!/bin/bash

# This script spins up a uvicorn server, #
# killing the last instance if running   #
# Have fun !				 #

public_address=`curl ifconfig.me`
port='8000'
startpage='docs'
app_dir=API_FastAPI

source '/home/ubuntu/fastapi-mysql/bin/activate'

pkill uvicorn
pkill python

echo Unite App Running available in http://$public_address:$port/$startpage 
echo --app-dir "/home/ubuntu/whosup/$app_dir" app:app --reload --host 0.0.0.0 --port $port
uvicorn --app-dir "/home/ubuntu/whosup/$app_dir" app:app --reload --host 0.0.0.0 --port $port

