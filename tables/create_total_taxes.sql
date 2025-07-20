CREATE TABLE total_taxes (
    total_tax_id UUID PRIMARY KEY,                                  -- NOT IN THE JSON FILE, IT WILL BE GENERATED USING PYTHON
    receipt_number TEXT REFERENCES receipts(receipt_number),        -- FOREIGN KEY
    id UUID,
    type TEXT, 
    name TEXT,
    rate NUMERIC,
    money_amount NUMERIC,
    UNIQUE (receipt_number, id)
);