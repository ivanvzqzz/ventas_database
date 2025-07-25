import json
import psycopg2
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

def generate_total_discount_id(receipt_number, discount_id):
    namespace = uuid.UUID("12345678-1234-5678-1234-567812345678")
    name = f"{receipt_number}-{discount_id}"
    return str(uuid.uuid5(namespace, name))

conn = psycopg2.connect(
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT")
)

cursor = conn.cursor()

with open("receipts.json", "r", encoding="utf-8") as f:
    receipts = json.load(f)

insert_total_discounts_query = """
INSERT INTO total_discounts (total_discount_id, receipt_number, id, 
                            type, name, percentage, money_amount)
VALUES (                    %s, %s, %s, 
                            %s, %s, %s, %s)
ON CONFLICT (receipt_number, id) DO NOTHING
"""

inserted_count = 0

