CREATE TABLE line_items (
    id UUID PRIMARY KEY,                                        -- UNIQUE
    receipt_number TEXT REFERENCES receipts(receipt_number),
    item_id UUID,
    variant_id UUID,
    item_name TEXT,
    variant_name TEXT,
    sku TEXT,
    quantity NUMERIC,
    price NUMERIC,
    gross_total_money NUMERIC,
    total_money NUMERIC,
    cost NUMERIC,
    cost_total NUMERIC,
    line_note TEXT,
    total_discount NUMERIC
);