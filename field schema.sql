create schema awards;
use awards;

create table studio(
id int primary key auto_increment,
name varchar(max) NOT NULL
);

create table producer(
id int primary key auto_increment,
name varchar(max) not null
);

create table Movie(
id int primary key auto_increment,
title varchar(max) not null,
winner boolean not null,
idStudio INTEGER ,
foreign key (idStudio ) references STUDIO(id)
);

create table movie_producer(
id int primary key auto_increment,
idProducer INTEGER NOT NULL,
idMovie INTEGER NOT NULL,
foreign key (idProducer ) references producer(id),
foreign key (idMovie ) references movie(id)
);