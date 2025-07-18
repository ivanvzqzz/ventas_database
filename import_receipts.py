import json
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

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

insert_receipt_query = """
INSERT INTO receipts (
    receipt_number, note, receipt_type, refund_for, order_info, created_at, updated_at,
    source, receipt_date, cancelled_at, total_money, total_tax, points_earned,
    points_deducted, points_balance, customer_id, total_discount, employee_id,
    store_id, pos_device_id, dining_option, tip, surcharge
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
ON CONFLICT (receipt_number) DO NOTHING;
"""
def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z') if value else None

inserted_count = 0

for receipt in receipts:

    cursor.execute(insert_receipt_query, (
        receipt.get("receipt_number"),
        receipt.get("note"),
        receipt.get("receipt_type"),
        receipt.get("refund_for"),
        json.dumps(receipt.get("order")) if receipt.get("order") else None,
        parse_date(receipt.get("created_at")),
        parse_date(receipt.get("updated_at")),
        receipt.get("source"),
        parse_date(receipt.get("receipt_date")),
        parse_date(receipt.get("cancelled_at")),
        receipt.get("total_money"),
        receipt.get("total_tax"),
        receipt.get("points_earned"),
        receipt.get("points_deducted"),
        receipt.get("points_balance"),
        receipt.get("customer_id"),
        receipt.get("total_discount"),
        receipt.get("employee_id"),
        receipt.get("store_id"),
        receipt.get("pos_device_id"),
        receipt.get("dining_option"),
        receipt.get("tip"),
        receipt.get("surcharge")  
    ))
    if cursor.rowcount == 1:
            inserted_count +=1

conn.commit()
if inserted_count == 0:
    print("No new records available.")
elif inserted_count == 1:
    print("✅ Updated sales database, added 1 record to total_taxes table.")
else:
    print(f"✅ Updated sales database, added {inserted_count} records to total_taxes table.")

cursor.close()
conn.close()