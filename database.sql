create database kisthack;
use kisthack;
create table student(
	id int not null auto_increment primary key ,
	name varchar(30) ,
    citizenship_number varchar (15),
     number varchar(10) ,
     address varchar (50),
     email varchar(40),
     DOB varchar(50),
     birthplace varchar(50)
     );
     
alter table student add column photo LONGBLOB;
alter table student add column frontphoto LONGBLOB;
