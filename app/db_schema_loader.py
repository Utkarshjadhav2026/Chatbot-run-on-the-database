import psycopg2

def fetch_schema_metadata(conn):
    cur = conn.cursor()

    # Tables + columns
    cur.execute("""
        SELECT
            c.table_name,
            c.column_name,
            c.data_type
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        ORDER BY c.table_name, c.ordinal_position;
    """)
    columns = cur.fetchall()

    # Row counts
    cur.execute("""
        SELECT
            relname AS table_name,
            n_live_tup AS row_count
        FROM pg_stat_user_tables;
    """)
    row_counts = dict(cur.fetchall())

    return columns, row_counts
