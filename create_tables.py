import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    conn = psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    def run_sql_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sql = f.read()

                cursor.execute(sql)
                conn.commit()
                print(f"Executed {file_path} successfully")
        except Exception as e:
            print(f"Error executing {file_path}: {e}")
            conn.rollback()

    def run_all_sql_files(tables_folder):
        for filename in os.listdir(tables_folder):
            if filename.endswith(".sql"):
                file_path = os.path.join(tables_folder, filename)
                run_sql_file(file_path)

    tables_folder = 'tables'

    run_all_sql_files(tables_folder)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()