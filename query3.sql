SELECT COUNT(Category.ItemID)
FROM Item, Category
WHERE Category.Num_Cat == 4 AND Category.ItemID == Item.ItemID