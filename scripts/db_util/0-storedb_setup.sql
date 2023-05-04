# This script creates the required database and user with admin privileges

# If you want to start from scratch run 'DROP DATABASE storedb;'
# as root from the mysql command line


CREATE DATABASE IF NOT EXISTS storedb;
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON storedb.* TO 'dev'@'localhost';