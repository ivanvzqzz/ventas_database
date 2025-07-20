CREATE TABLE line_taxes (
    line_tax_id UUID PRIMARY KEY,                   			-- NOT IN THE JSON FILE, IT WILL BE GENERATED IN PYTHON BASED ON LINE ID
	receipt_number TEXT REFERENCES receipts(receipt_number),	-- HIGHER-LEVEL REFERENCE
    line_items_id UUID REFERENCES line_items(id),  				-- FOREIGN KEY
    money_amount NUMERIC,
    tax_type_id UUID,
    type TEXT,
    name TEXT,
    rate NUMERIC,
    UNIQUE (tax_type_id, line_items_id)
);