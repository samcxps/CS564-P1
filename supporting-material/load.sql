.separator |
.import category.dat Category
.import bid.dat Bid
.import user.dat User
.import item.dat Item
update Item set Buy_Price = null where Buy_Price = 'NULL'