
# from agno.tools import tool
# from db import get_connection

# @tool
# def run_sql(query: str):
#     """Execute SQL query and return rows"""
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute(query)
#     rows = cur.fetchall()
#     cols = [desc[0] for desc in cur.description]

#     cur.close()
#     conn.close()

#     return {
#         "columns": cols,
#         "rows": rows
#     }

from db import get_connection
from knowledge import load_schema_knowledge,load_sample_examples

MAX_SCHEMA_CHARS = 12000


def get_schema_context(question: str = "") -> str:
    """
    Returns schema + sample data (shortened) to avoid token overflow.
    Optional: question is kept for future filtering improvements.
    """
    text = load_schema_knowledge()

    text = "NOTE: Tables are written as public.TableName (example: public.TourTracking).\n\n" + text

    if len(text) > MAX_SCHEMA_CHARS:
        return text[:MAX_SCHEMA_CHARS] + "\n\n... (truncated to avoid token overflow)"

    return text


def run_sql(query: str, limit: int = 50):
    """
    Executes SQL query and returns rows as list[dict].
    Adds LIMIT automatically if missing.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        q = query.strip().rstrip(";") #clean query, remove extra space and ; from the end

        # enforce limit for safety
        if "limit" not in q.lower():
            q = f"{q} LIMIT {limit}"

        cur.execute(q)

        # if query returns rows (SELECT)
        if cur.description:
            col_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(col_names, row)) for row in rows]

        conn.commit()
        return {"message": "Query executed successfully"}

    finally:
        cur.close()
        conn.close()
