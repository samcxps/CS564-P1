drop table if exists Bid;
drop table if exists Category;
drop table if exists Item;
drop table if exists User;

create table Bid (ItemID int PRIMARY KEY, FOREIGN KEY (ItemID) REFERENCES Item (ItemID), UserID char(255) PRIMARY KEY, FOREIGN KEY (UserID) REFERENCES User (UserID), Time char(255), Amount float);
create table Category (ItemID int PRIMARY KEY, FOREIGN KEY (ItemID) REFERENCES Item (ItemID), Category_val char(255));
create table Item (ItemID int PRIMARY KEY, Name char(255), Currently float, Buy_Price float, First_Bid float, Number_of_Bids int, Start char(255), End char(255), SellerID char(255), FOREIGN KEY (SellerID) REFERENCES User (UserID), Description char(255));
create table User (UserID char(255) PRIMARY KEY, Rating int, Country char(255), Location char(255));