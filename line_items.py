import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def insert_line_items():
    conn = psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    with open ("receipts.json", "r", encoding="utf-8") as f:
        receipts = json.load(f)

    insert_line_items_query = """
    INSERT INTO line_items (id, receipt_number, item_id, variant_id, item_name, variant_name, sku,
                            quantity, price, gross_total_money, total_money, cost, cost_total, line_note,
                            total_discount)
    VALUES (
                            %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s,
                            %s)
    ON CONFLICT (id) DO NOTHING;
    """

    inserted_count = 0

    for receipt in receipts:
        receipt_number = receipt.get("receipt_number")
        line_items = receipt.get("line_items", [])

        for item in line_items:
            cursor.execute(insert_line_items_query, (
                item.get("id"),
                receipt_number,
                item.get("item_id"),
                item.get("variant_id"),
                item.get("item_name"),
                item.get("variant_name"),
                item.get("sku"),
                item.get("quantity"),
                item.get("price"),
                item.get("gross_total_money"),
                item.get("total_money"),
                item.get("cost"),
                item.get("cost_total"),
                item.get("line_note"),
                item.get("total_discount")
            ))
            if cursor.rowcount == 1:
                inserted_count +=1

    conn.commit()
    if inserted_count == 0:
        print("No new records available")
    elif inserted_count == 1:
        print("Updated sales database, added 1 record to line_items table.")
    else:
        print(f"Updated sales database, added {inserted_count} records to line_items table.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_line_items()