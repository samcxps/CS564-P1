WITH Total AS (SELECT DISTINCT Category.Category_1 FROM Category, Bid WHERE Category.Category_1 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        UNION
        SELECT DISTINCT Category.Category_2 FROM Category, Bid WHERE Category.Category_2 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        UNION
        SELECT DISTINCT Category.Category_3 FROM Category, Bid WHERE Category.Category_3 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        UNION
        SELECT DISTINCT Category.Category_4 FROM Category, Bid WHERE Category.Category_4 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        UNION
        SELECT DISTINCT Category.Category_5 FROM Category, Bid WHERE Category.Category_5 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        UNION
        SELECT DISTINCT Category.Category_6 FROM Category, Bid WHERE Category.Category_6 IS NOT NULL AND Bid.ItemID == Category.ItemID AND Bid.Amount > 100
        )
SELECT COUNT(*)
FROM Total
