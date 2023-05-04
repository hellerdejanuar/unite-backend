# If you want to start from scratch run 'DROP DATABASE storedb;'
# as root from the mysql command line

CREATE DATABASE IF NOT EXISTS storedb;
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON storedb.* TO 'dev'@'localhost';

USE storedb;

# Create ' user_profile ' table and initialize with data

CREATE TABLE IF NOT EXISTS "user" (
  id        INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  name      VARCHAR(255),
  email     VARCHAR(255),
  password  VARCHAR(255),
  phone     VARCHAR(255)
);

INSERT INTO "user" (name, email, password, phone)
VALUES ('Jorge', 'keeponjorging@gmail.com', 'afefina', '0059894332244'),
       ('Marito', 'maritobaracus@gmail.com', 'fdadgijkko', '005466554433'),
       ('Valentina', 'vdevalentina@gmail.com', 'nenemalo', '0059899467367');

# Create ' event ' table and initialize with data
CREATE TABLE IF NOT EXISTS events (
  id              INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  event_name      VARCHAR(225),
  event_datetime  VARCHAR(225),
  location        VARCHAR(225),
  description     VARCHAR(225),
  participants    VARCHAR(225),
  event_status    VARCHAR(225),
  nonolist        VARCHAR(225)
);
