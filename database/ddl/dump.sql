
-- Tables Section
-- _____________ 

create table users (
     id int not null auto_increment,
     firstname varchar(50) not null,
     lastname varchar(50) not null,
     address varchar(100) not null,
     coordinates POINT,
     constraint ID_User_ID primary key (id));

create table account (
     number varchar(50) not null,
     balance float(15,2) not null,
     user_id int not null,
     constraint ID_Account_ID primary key (number));
	 
create table transfer (
     id int not null auto_increment,
     amount float(10) not null,
     date datetime not null default CURRENT_TIMESTAMP(),
     from_acc varchar(50) not null,
     to_acc varchar(50) not null,
     constraint ID_Transfer_ID primary key (id));


-- Constraints Section
-- ___________________ 

alter table account add constraint FKowns_FK
     foreign key (user_id)
     references users (id);

alter table transfer add constraint FKto_FK
     foreign key (from_acc)
     references account (number);

alter table transfer add constraint FKfrom_FK
     foreign key (to_acc)
     references account (number);

-- Index Section
-- _____________ 

create unique index ID_User_IND
     on users (id);

create unique index ID_Account_IND
     on account (number);

create index FKowns_IND
     on account (user_id);
	 
create unique index ID_Transfer_IND
     on transfer (id);

create index FKto_IND
     on transfer (from_acc);

create index FKfrom_IND
     on transfer (to_acc);

