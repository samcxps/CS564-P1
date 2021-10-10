SELECT COUNT(User.UserID)
FROM Seller, User
WHERE User.Rating > 1000 AND Seller.UserID == User.UserID