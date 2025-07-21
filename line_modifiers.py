import json
import psycopg2
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

def generate_line_modifiers_id(modifier_id, item_id):
    namespace = uuid.UUID("12345678-1234-5678-1234-567812345678")
    name = f"{modifier_id}-{item_id}"
    return str(uuid.uuid5(namespace, name))

def insert_line_modifiers():
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

    insert_line_modifiers_query = """
    INSERT INTO line_modifiers (id, receipt_number, line_items_id, line_modifier_id, modifier_option_id,
                                name, option, price, money_amount)
    VALUES(
                                %s, %s, %s, %s, %s,
                                %s, %s, %s, %s
                                )
    ON CONFLICT (line_modifier_id, line_items_id) DO NOTHING
    """

    inserted_count = 0

    for receipt in receipts:
        receipt_number = receipt.get("receipt_number")
        
        for line_item in receipt.get("line_items", []):
            line_items_id = line_item.get("id")

            for item in line_item.get("line_modifiers", []):
                cursor.execute(insert_line_modifiers_query, (
                    generate_line_modifiers_id(item.get("id"), line_items_id),
                    receipt_number,
                    line_items_id,
                    item.get("id"),
                    item.get("modifier_option_id"),
                    item.get("name"),
                    item.get("option"),
                    item.get("price"),
                    item.get("money_amount")
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
    insert_line_modifiers()