CREATE TABLE payments (
    payment_id UUID PRIMARY KEY,                                -- NOT IN THE JSON FILE, IT WILL BE GENERATED WITH PYTHON
    receipt_number TEXT REFERENCES receipts(receipt_number),
    payment_type_id UUID,
    name TEXT,
    type TEXT,
    money_amount NUMERIC,
    paid_at TIMESTAMP,
    payment_details JSONB
);