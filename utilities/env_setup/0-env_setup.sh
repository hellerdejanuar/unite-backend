#!/usr/bin/env bash

COLOR='\033[0;35m'
NOCOLOR='\033[0m'

# Programs
sudo apt-get update -y

echo -e "${COLOR}Instalando: mysql${NOCOLOR}"
sudo apt-get install -y mysql-server=8.0.30

echo -e "${COLOR}Instalando: python${NOCOLOR}"
sudo apt-get install -y python=3.8.10

echo -e "${COLOR}Instalando: pip${NOCOLOR}"
sudo apt-get install -y python3-pip



# Python virtual environment
echo -e "${COLOR}Instalando: venv${NOCOLOR}"
sudo apt-get install -y python3-venv

echo -e "${COLOR}Creando entorno virtual${NOCOLOR}"
sudo python3 -m venv ./fastapi-mysql 
sudo chown -R ubuntu:ubuntu ./fastapi-mysql/

echo -e "${COLOR}Activando entorno virtual${NOCOLOR}"
source fastapi-mysql/bin/activate


# Python libraries to be installed
# inside the venv

echo -e "${COLOR}Instalando: wheel${NOCOLOR}"
pip install wheel

echo -e "${COLOR}Instalando: uvicorn${NOCOLOR}"
pip install uvicorn==0.18.3

echo -e "${COLOR}Instalando: fastapi${NOCOLOR}"
pip install fastapi[all] 

echo -e "${COLOR}Instalando: sqlalchemy${NOCOLOR}"
pip install sqlalchemy 

echo -e "${COLOR}Instalando: pymysql${NOCOLOR}"
pip install pymysql==1.0.2 

#echo -e "${COLOR}Instalando: httptools${NOCOLOR}"
#pip install httptools==0.1.2 

echo -e "${COLOR}Instalando: cryptography${NOCOLOR}"
pip install cryptography
