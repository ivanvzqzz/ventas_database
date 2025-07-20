CREATE TABLE line_discounts (
    id UUID PRIMARY KEY,                                        -- NOT IN THE JSON FILE, IT WILL BE GENERATED WITH PYTHON
    receipt_number TEXT REFERENCES receipts(receipt_number),    -- FOREIGN KEY
    line_items_id UUID REFERENCES line_items(id),               -- FOREIGN KEY
    line_discount_id UUID,
    type TEXT,
    name TEXT,
    percentage NUMERIC,
    money_amount NUMERIC,
    UNIQUE (line_items_id, line_discount_id)
);