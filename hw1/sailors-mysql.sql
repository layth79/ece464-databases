/*
SQL queries to populate a Sailors and Boats dataset
*/
create table sailors(
    sid int PRIMARY KEY,
    sname varchar(30),
    rating int,
    age int
);

create table reserves(
    sid int,
    bid int,
    day date,
    PRIMARY KEY (sid, bid, day)
);

create table boats(
    bid int PRIMARY KEY,
    bname char(20),
    color char(10),
    length int
);

create table employees(
    eid int PRIMARY KEY,
    ename varchar(30),
    job varchar(30)
);

create table addresses(
    aid int PRIMARY KEY,
    eid int,
    zip int,
    line1 varchar(30),
    line2 varchar(30),
    city varchar(20)
);

create table salaries(
    salid int PRIMARY KEY,
    eid int,
    weeklyhrs int,
    hourlypay int,
    overtimehrs int,
    overtimepay int
);

insert into employees values (200, 'john', 'cleaner');
insert into employees values (201, 'andy', 'cleaner');
insert into employees values (202, 'carl', 'repairman');
insert into employees values (203, 'benedict', 'repairman');
insert into employees values (204, 'juan', 'accountant');
insert into employees values (205, 'trevor', 'driver');
insert into employees values (206, 'james', 'driver');

insert into addresses values (300, 200, 11365, '40 henry smith ave', NULL, 'fresh meadows');
insert into addresses values (301, 201, 11463, '7948 randall road', NULL, 'garden city');
insert into addresses values (302, 202, 11712, '65 arcadia lane', '4th floor', 'port jefferson');
insert into addresses values (303, 203, 11125, '40 henry smith ave', NULL, 'hempstead');
insert into addresses values (304, 204, 11298, '6 inverness dr', '2nd floor', 'greenport');
insert into addresses values (305, 205, 11445, '94 york st', '3rd floor', 'fresh meadows');
insert into addresses values (306, 206, 11268, '7 sycamore ave', NULL, 'greenport');

insert into salaries values (400, 200, 40, 15, 5, 20);
insert into salaries values (401, 201, 40, 15, 2, 20);
insert into salaries values (402, 202, 40, 25, 0, 35);
insert into salaries values (403, 203, 50, 35, 0, 50);
insert into salaries values (404, 204, 45, 45, 5, 60);
insert into salaries values (405, 205, 20, 15, 0, 20);
insert into salaries values (406, 206, 50, 15, 0, 20);

insert into sailors values (22,'dusting',7,45);
insert into sailors values (29,'brutus',1,33);
insert into sailors values (31,'lubber',8,55);
insert into sailors values (32,'andy',8,25);
insert into sailors values (58,'rusty',10,35);
insert into sailors values (64,'horatio',7,16);
insert into sailors values (71,'zorba',10,35);
insert into sailors values (74,'horatio',9,25);
insert into sailors values (85,'art',3,25);
insert into sailors values (95,'bob',3,63);
insert into sailors values (23,'emilio',7,45);
insert into sailors values (24,'scruntus',1,33);
insert into sailors values (35,'figaro',8,55);
insert into sailors values (59,'stum',8,25);
insert into sailors values (60,'jit',10,35);
insert into sailors values (61,'ossola',7,16);
insert into sailors values (62,'shaun',10,35);
insert into sailors values (88,'dan',9,25);
insert into sailors values (89,'dye',3,25);
insert into sailors values (90,'vin',3,63);

insert into reserves values (23,104,'1998/10/10');
insert into reserves values (24,104,'1998/10/10');
insert into reserves values (35,104,'1998/8/10');
insert into reserves values (59,105,'1998/7/10');
insert into reserves values (23,105,'1998/11/10');
insert into reserves values (35,105,'1998/11/6');
insert into reserves values (59,106,'1998/11/12');
insert into reserves values (60,106,'1998/9/5');
insert into reserves values (60,106,'1998/9/8');
insert into reserves values (88,107,'1998/9/8');
insert into reserves values (89,108,'1998/10/10');
insert into reserves values (90,109,'1998/10/10');
insert into reserves values (89,109,'1998/8/10');
insert into reserves values (60,109,'1998/7/10');
insert into reserves values (59,109,'1998/11/10');
insert into reserves values (62,110,'1998/11/6');
insert into reserves values (88,110,'1998/11/12');
insert into reserves values (88,110,'1998/9/5');
insert into reserves values (88,111,'1998/9/8');
insert into reserves values (61,112,'1998/9/8');
insert into reserves values (22,101,'1998/10/10');
insert into reserves values (22,102,'1998/10/10');
insert into reserves values (22,103,'1998/8/10');
insert into reserves values (22,104,'1998/7/10');
insert into reserves values (31,102,'1998/11/10');
insert into reserves values (31,103,'1998/11/6');
insert into reserves values (31,104,'1998/11/12');
insert into reserves values (64,101,'1998/9/5');
insert into reserves values (64,102,'1998/9/8');
insert into reserves values (74,103,'1998/9/8');

insert into boats values (101,'Interlake','blue', 45);
insert into boats values (102,'Interlake','red', 45);
insert into boats values (103,'Clipper','green', 40);
insert into boats values (104,'Clipper','red', 40);
insert into boats values (105,'Marine','red', 35);
insert into boats values (106,'Marine','green', 35);
insert into boats values (107,'Marine','blue', 35);
insert into boats values (108,'Driftwood','red', 35);
insert into boats values (109,'Driftwood','blue', 35);
insert into boats values (110,'Klapser','red', 30);
insert into boats values (111,'Sooney','green', 28);
insert into boats values (112,'Sooney','red', 28);
