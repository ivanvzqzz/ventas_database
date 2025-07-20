CREATE TABLE total_discounts (
    total_discount_id UUID PRIMARY KEY,
    receipt_number TEXT REFERENCES receipts(receipt_number),
    id UUID,
    type TEXT,
    name TEXT,
    percentage NUMERIC,
    money_amount NUMERIC
    UNIQUE (receipt_number, id)
);