
# import json
# from agno.knowledge import Knowledge

# def load_schema_knowledge() -> Knowledge:
#     with open("schema.json") as f:
#         schema = json.load(f)

#     text = ""

#     for table, columns in schema.items():
#         text += f"Table: {table}\nColumns:\n"
#         for col in columns:
#             text += f"- {col['column']} ({col['type']})\n"
#         text += "\n"

#     # ⚠️ IMPORTANT: positional argument ONLY
#     return Knowledge(text.strip())

import json
from agno.knowledge import Knowledge

def load_schema_knowledge() -> Knowledge:
    with open("schema.json") as f:
        schema = json.load(f)

    text = ""

    for table, meta in schema.items():
        text += f"Table: {table}\n"
        text += f"Description: {meta['description']}\n"
        text += f"Primary Key: {meta['primary_key']}\n"
        text += f"Approx Rows: {meta['row_count']}\n"
        text += "Columns:\n"

        for col in meta["columns"]:
            text += (
                f"- {col['name']} ({col['type']}): "
                f"{col['description']}\n"
            )

        text += "\n"

    # IMPORTANT: positional argument only
    return Knowledge(text.strip())


def load_sample_examples() -> Knowledge:
    """
    Loads example rows per table.
    JSON format:
    {
      "TableName": [ {col: value}, {col: value} ]
    }
    """

    with open("table_examples.json") as f:
        data = json.load(f)

    text_parts = []

    for table, rows in data.items():
        # Safety checks
        if not isinstance(rows, list) or not rows:
            continue

        text_parts.append(f'Table "{table}" example rows:')

        for row in rows[:5]:
            text_parts.append(str(row))

        text_parts.append("")  # spacing

    return Knowledge("\n".join(text_parts).strip())

def load_table_examples() -> Knowledge:
    import json
    from agno.knowledge import Knowledge

    with open("table_examples.json") as f:
        data = json.load(f)

    text = ""

    for table, rows in data.items():
        text += f'Table "{table}" example rows:\n'

        if not isinstance(rows, list):
            continue

        for row in rows[:5]:
            text += f"{row}\n"

        text += "\n"

    return Knowledge(text.strip())
