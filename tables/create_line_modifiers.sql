CREATE TABLE line_modifiers (
    id UUID PRIMARY KEY,                                        -- NOT IN THE JSON FILE, IT WILL BE GENERATED WITH PYTHON
    receipt_number TEXT REFERENCES receipts(receipt_number),    -- FOREIGN KEY
    line_items_id UUID REFERENCES line_items(id),               -- FOREIGN KEY
    line_modifier_id UUID,
    modifier_option_id UUID,
    name TEXT,
    option TEXT,
    price NUMERIC,
    money_amount NUMERIC,
    UNIQUE (line_modifier_id, line_items_id)
);