SELECT COUNT(Seller.UserID)
FROM Seller, Bidder
WHERE Bidder.UserID == Seller.UserID