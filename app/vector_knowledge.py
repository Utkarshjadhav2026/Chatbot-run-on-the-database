from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.sql import SQLTools
from agno.tools.reasoning import ReasoningTools
from agno.knowledge import Knowledge

DB_URL = "postgresql://postgres:wemotive%401234@localhost:5432/mydatabase"


def load_schema_knowledge() -> Knowledge:
    with open("schema.json") as f:
        return Knowledge(f.read())

def load_table_examples() -> Knowledge:
    with open("table_examples.json") as f:
        return Knowledge(f.read())

def load_sample_queries() -> Knowledge:
    with open("sample_query.json") as f:
        return Knowledge(f.read())

sql_agent_knowledge = [
    load_schema_knowledge(),
    load_table_examples(),
    load_sample_queries(),
]


system_message = """
You are a PostgreSQL database assistant.

Rules:
- Table names are case-sensitive and start with a capital letter (e.g. "Tour").
- Column names are case-sensitive and must match schema exactly.
- ALWAYS wrap table and column names in double quotes.
- NEVER guess, pluralize, or rename tables or columns.
- If a column is BIGINT time (epoch ms), use to_timestamp(col / 1000).
- If a question is ambiguous, ask ONE clarification question.
- Before writing SQL, call sql_agent_knowledge to verify exact names.
- If the question is clear, generate SQL and execute it.
- Return generated query and only the database result.
"""

def save_validated_query(query: str):
    with open("validated_queries.log", "a") as f:
        f.write(query + "\n")


sql_agent = Agent(
    name="SQL Agent",
    model=Gemini(
        id="gemini-2.5-pro"  # ✅ stable & supported
    ),   
    knowledge=sql_agent_knowledge,
    system_message=system_message,
    tools=[
        SQLTools(db_url=DB_URL),
        ReasoningTools(add_instructions=True),
        save_validated_query,
    ],
    add_datetime_to_context=True,
    enable_agentic_memory=True,
    search_knowledge=True,
    add_history_to_context=True,
    num_history_runs=5,
    read_chat_history=True,
    read_tool_call_history=True,
    markdown=True,
)

# from agno.os import AgentOS

# agent_os = AgentOS(agents=[sql_agent])
# app = agent_os.get_app()

# if __name__ == "__main__":
#     agent_os.serve(app="vector_knowledge:app", reload=True)

if __name__ == "__main__":
    print("SQL Agent ready (type 'exit' to quit)\n")

    while True:
        question = input("Ask DB Question (or exit): ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        response = sql_agent.run(question)
        print("\n--- RESULT ---")
        print(response.content)
        print("--------------\n")
