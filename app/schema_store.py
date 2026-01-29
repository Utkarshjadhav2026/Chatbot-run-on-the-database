import json
from extract_schema import extract_schema

SCHEMA_FILE = "schema.json"

def generate_schema_json():
    schema = extract_schema()
    with open(SCHEMA_FILE, "w") as f:
        json.dump(schema, f, indent=2)

    print("✅ schema.json generated from PostgreSQL")

if __name__ == "__main__":
    generate_schema_json()
