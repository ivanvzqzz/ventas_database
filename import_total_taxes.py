import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT")
)

cursor = conn.cursor()

with open ("receipts.json", "r") as f:
    receipts = json.load(f)

insert_total_taxes_query = """
INSERT INTO total_taxes (receipt_number, id, type, name, rate, money_amount)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (receipt_number, id) DO NOTHING;
"""

inserted_count = 0

for receipt in receipts:
    receipt_number = receipt.get("receipt_number")
    total_taxes = receipt.get("total_taxes", [])

    for tax in total_taxes:
        cursor.execute(insert_total_taxes_query, (
            receipt_number,
            tax.get("id"),
            tax.get("type"),
            tax.get("name"),
            tax.get("rate"),
            tax.get("money_amount")
        ))
        if cursor.rowcount == 1:
            inserted_count +=1

conn.commit()
if inserted_count == 0:
    print("No new records available")
elif inserted_count == 1:
    print("✅ Updated sales database, added 1 record to total_taxes table.")
else:
    print(f"✅ Updated sales database, added {inserted_count} records to total_taxes table.")

cursor.close()
conn.close()