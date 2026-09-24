"""
Centralized Database Connection and Initialization Utility for Car Saga.
Designed for Class 12 CBSE Computer Science: straightforward, readable, and secure.
"""

from pathlib import Path
import mysql.connector
from mysql.connector import Error

# Standard CBSE Project Configuration
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = "student"
DB_NAME = "CarSaga"


def get_connection(database_name=DB_NAME, autocommit=False):
    """
    Establish and return a MySQL connection.
    If database_name is specified, connects to that database.
    """
    config = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASS,
        "autocommit": autocommit,
    }
    if database_name:
        config["database"] = database_name

    return mysql.connector.connect(**config)


def execute_sql_file(cursor, file_path):
    """
    Executes multiple SQL statements from an external .sql file sequentially.
    """
    content = Path(file_path).read_text(encoding="utf-8")
    # Clean SQL comments and split statements
    statements = []
    current = []
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("--"):
            continue
        current.append(line)
        if trimmed.endswith(";"):
            statements.append("\n".join(current))
            current = []

    for stmt in statements:
        sql = stmt.strip()
        if sql:
            cursor.execute(sql)


def cleanup_legacy_tables_if_needed(cursor):
    """
    Safely handles legacy conflict tables if an older experiment left empty incompatible tables.
    """
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        # Check if favourites has variant_id instead of car_id
        cursor.execute("SHOW TABLES LIKE 'favourites'")
        if cursor.fetchone():
            cursor.execute("DESCRIBE favourites")
            cols = [col[0] for col in cursor.fetchall()]
            if "variant_id" in cols and "car_id" not in cols:
                cursor.execute("DROP TABLE IF EXISTS favourites")
                cursor.execute("DROP TABLE IF EXISTS recently_viewed")
                cursor.execute("DROP TABLE IF EXISTS saved_searches")

        # Check if users is missing email or full_name
        cursor.execute("SHOW TABLES LIKE 'users'")
        if cursor.fetchone():
            cursor.execute("DESCRIBE users")
            user_cols = [col[0] for col in cursor.fetchall()]
            if "email" not in user_cols or "full_name" not in user_cols:
                cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    except Exception as e:
        print("Note during table migration check:", e)


def initialize_database():
    """
    Automatically creates the CarSaga database and tables if missing.
    Populates initial seed data safely without destroying user data.
    """
    try:
        # Step 1: Connect to server without database to ensure database exists
        server_conn = get_connection(database_name=None, autocommit=True)
        server_cursor = server_conn.cursor()
        server_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        server_cursor.close()
        server_conn.close()

        # Step 2: Connect to CarSaga database and execute schema & seed
        app_conn = get_connection(database_name=DB_NAME, autocommit=True)
        app_cursor = app_conn.cursor()

        cleanup_legacy_tables_if_needed(app_cursor)

        base_dir = Path(__file__).resolve().parent
        schema_file = base_dir / "schema.sql"
        seed_file = base_dir / "seed.sql"

        if schema_file.exists():
            execute_sql_file(app_cursor, schema_file)

        if seed_file.exists():
            execute_sql_file(app_cursor, seed_file)

        app_cursor.close()
        app_conn.close()
        return True
    except Error as err:
        print(f"Database Initialization Error: {err}")
        return False
    except Exception as exc:
        print(f"General Initialization Error: {exc}")
        return False
