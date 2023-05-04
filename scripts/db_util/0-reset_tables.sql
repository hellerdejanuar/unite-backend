# This script deletes and creates the required database and user with admin privileges

DROP DATABASE storedb;
CREATE DATABASE storedb;
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON storedb.* TO 'dev'@'localhost';