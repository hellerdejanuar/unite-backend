# This script creates inserts dummy data into the

USE storedb;

INSERT INTO users (name, email, password, phone)
VALUES ('Jorge', 'keeponjorging@gmail.com', 'afefina', '0059894332244'),
       ('Marito', 'maritobaracus@gmail.com', 'fdadgijkko', '005466554433'),
       ('Valentina', 'vdevalentina@gmail.com', 'nenemalo', '0059899467367');
