CREATE SCHEMA IF NOT EXISTS awards;
USE awards;

CREATE TABLE IF NOT EXISTS studio(
id int primary key auto_increment,
name varchar(max) NOT NULL
);

CREATE TABLE IF NOT EXISTS producer(
id int primary key auto_increment,
name varchar(max) not null
);

CREATE TABLE IF NOT EXISTS Movie(
id int primary key auto_increment,
title varchar(max) not null,
winner boolean not null,
release INTEGER not null
);

CREATE TABLE IF NOT EXISTS MovieProducer(
id int primary key auto_increment,
idProducer INTEGER NOT NULL,
idMovie INTEGER NOT NULL,
foreign key (idProducer ) references producer(id),
foreign key (idMovie ) references movie(id)
);

CREATE TABLE IF NOT EXISTS MovieStudio(
id int primary key auto_increment,
idStudio INTEGER NOT NULL,
idMovie INTEGER NOT NULL,
foreign key (idStudio ) references Studio(id),
foreign key (idMovie ) references movie(id)
);