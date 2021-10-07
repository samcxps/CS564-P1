SELECT COUNT(Item.SellerID)
FROM Item, Bid
WHERE Bid.UserID == Item.SellerID