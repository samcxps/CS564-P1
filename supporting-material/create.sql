drop table if exists Bid;
drop table if exists Category;
drop table if exists Item;
drop table if exists User;

create table Bid (ItemID int PRIMARY KEY, UserID char(255) PRIMARY KEY, Time char(255), Amount float);
create table Category (ItemID int PRIMARY KEY, Category_val char(255));
create table Item (ItemID int PRIMARY KEY, Name char(255), Currently float, Buy_Price float, First_Bid float, Number_of_Bids int, Start char(255), End char(255), SellerID char(255), Description char(255));
create table User (UserID char(255) PRIMARY KEY, Rating int, Country char(255), Location char(255));