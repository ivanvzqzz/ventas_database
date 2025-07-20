CREATE TABLE total_discounts (
    total_discount_id UUID PRIMARY KEY,                             -- NOT IN THE JSON FILE, IT WILL BE GENERATED IN PYTHON
    receipt_number TEXT REFERENCES receipts(receipt_number),
    id UUID,
    type TEXT,
    name TEXT,
    percentage NUMERIC,
    money_amount NUMERIC,
    UNIQUE (receipt_number, id)
);