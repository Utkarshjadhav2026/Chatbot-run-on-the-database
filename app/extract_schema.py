# import psycopg2
# from collections import defaultdict

# DB_CONFIG = {
#     "dbname": "mydatabase",
#     "user": "postgres",
#     "password": "wemotive@1234",
#     "host": "localhost",
#     "port": 5432,
# }

# def extract_schema() -> dict:
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT table_name, column_name, data_type
#         FROM information_schema.columns
#         WHERE table_schema = 'public'
#         ORDER BY table_name, ordinal_position
#     """)

#     schema = defaultdict(list)

#     for table, column, dtype in cur.fetchall():
#         schema[table].append({
#             "column": column,
#             "type": dtype
#         })

#     cur.close()
#     conn.close()
#     return dict(schema)


import psycopg2
from collections import defaultdict
from db import get_connection

def extract_schema() -> dict:
    conn = get_connection()
    cur = conn.cursor()

    # -------------------------------
    # Columns + descriptions
    # -------------------------------
    cur.execute("""
        SELECT
            c.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            pgd.description
        FROM information_schema.columns c
        LEFT JOIN pg_catalog.pg_statio_all_tables st
            ON c.table_schema = st.schemaname
           AND c.table_name = st.relname
        LEFT JOIN pg_catalog.pg_description pgd
            ON pgd.objoid = st.relid
           AND pgd.objsubid = c.ordinal_position
        WHERE c.table_schema = 'public'
        ORDER BY c.table_name, c.ordinal_position;
    """)

    tables = defaultdict(lambda: {
        "description": "",
        "primary_key": "",
        "row_count": 0,
        "columns": []
    })

    for table, col, dtype, nullable, desc in cur.fetchall():
        tables[table]["columns"].append({
            "name": col,
            "type": dtype,
            "nullable": nullable == "YES",
            "description": desc or ""
        })

    # -------------------------------
    # Primary Keys
    # -------------------------------
    cur.execute("""
        SELECT
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = 'public';
    """)

    for table, pk in cur.fetchall():
        tables[table]["primary_key"] = pk

    # -------------------------------
    # Approx row counts (FAST)
    # -------------------------------
    cur.execute("""
        SELECT relname, reltuples::BIGINT
        FROM pg_class
        WHERE relkind = 'r';
    """)

    for table, count in cur.fetchall():
        if table in tables:
            tables[table]["row_count"] = count

    cur.close()
    conn.close()

    return dict(tables)
