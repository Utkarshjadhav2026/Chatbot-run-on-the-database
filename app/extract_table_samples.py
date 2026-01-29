import json
from db import get_connection

MAX_ROWS_PER_TABLE = 3


def extract_table_examples() -> dict:
    conn = get_connection()
    cur = conn.cursor()

    # --------------------------------
    # Get all public tables
    # --------------------------------
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE';
    """)

    tables = [row[0] for row in cur.fetchall()]
    data = {}

    for table in tables:
        try:
            cur.execute(f'''
                SELECT *
                FROM "{table}"
                LIMIT {MAX_ROWS_PER_TABLE};
            ''')

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            # Direct list of rows (NO wrapper keys)
            data[table] = [
                dict(zip(columns, row))
                for row in rows
            ]

        except Exception:
            # If unreadable → empty list (never break JSON)
            data[table] = []

    cur.close()
    conn.close()
    return data


if __name__ == "__main__":
    examples = extract_table_examples()

    with open("table_examples.json", "w") as f:
        json.dump(examples, f, indent=2, default=str)

    print("✅ table_examples.json generated successfully")
