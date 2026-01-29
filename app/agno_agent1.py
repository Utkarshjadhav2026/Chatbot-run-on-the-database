# from agno.agent import Agent
# from model import model
# from knowledge import load_schema_knowledge
# from tools import run_sql

# schema_knowledge = load_schema_knowledge()

# agent = Agent(
#     model=model,
#     knowledge=[schema_knowledge],
#     tools=[run_sql],
#     instructions=[
#         "You are a PostgreSQL execution agent, not a chatbot.",
#         "You MUST ALWAYS answer by running SQL using the run_sql tool.",
#         "You are NOT allowed to ask follow-up questions.",
#         "If the user asks about data, you MUST infer the correct table from schema.",
#         "If multiple tables exist, choose the most relevant one.",
#         "If a c olumn does not exist, return an empty result, not an explanation.",
#         "Your final answer MUST be the SQL result, not text.",
#         "NEVER apologize.",
#         "NEVER say you cannot verify schema."
#     ]
# )

from agno.agent import Agent
from model import model
from knowledge import load_schema_knowledge,load_table_examples, load_sample_examples
from tools import run_sql,get_schema_context
from agno.db.sqlite import SqliteDb


# schema_knowledge = load_schema_knowledge()
schema_knowledge = load_schema_knowledge()
sample_knowledge = load_table_examples()
query_knowledge = load_sample_examples()
total_knowledge = [schema_knowledge, sample_knowledge, query_knowledge]
agent = Agent(
    model=model,
    knowledge=total_knowledge,
    tools=[run_sql,get_schema_context],
    instructions = [
            "You are a PostgreSQL database assistant chatbot.",
            "You MUST answer using the database.",
            "Before writing SQL, always check schema context using load_schema_knowledge().",
            "Only use tables and columns that exist in the schema context.",
            "If user asks for top/most/count/trends, generate SQL and execute using run_sql().",
            "If filtering by year/month/day, prefer timestamp columns like createdAt",
            "If the column values are null try to filter on similar start name columns by conformation with the sample_knowledge"
            "If a time column is bigint, treat it as epoch milliseconds unless proven otherwise.",
            "Return final answer as it is the query returns",
    ],
    markdown=True
)


schema_agent = Agent(
    model=model,
    knowledge=[schema_knowledge],
    instructions=[
        "You are a PostgreSQL schema expert.",
        "You ONLY understand tables and columns.",
        "Never write SQL.",
        "Never invent columns.",
        "Answer only which tables and columns are relevant."
    ],
    markdown=False
)

query_agent = Agent(
    model=model,
    knowledge=[query_knowledge],
    instructions=[
        "You convert user questions into PostgreSQL SQL.",
        "Use ONLY column names confirmed by schema_agent.",
        "If time column is BIGINT, treat it as epoch milliseconds.",
        "Use to_timestamp(column / 1000.0) for time filtering.",
        "Never explain SQL.",
        "Output ONLY SQL."
    ],
    markdown=False
)

executor_agent = Agent(
    model=model,
    knowledge=[sample_knowledge],
    tools=[run_sql],
    instructions=[
        "You are a PostgreSQL execution agent.",
        "You MUST execute the given SQL using run_sql.",
        "Do NOT modify the SQL.",
        "Do NOT explain results.",
        "Return ONLY the query result in table format.",
        "If SQL fails, return empty table."
    ],
    markdown=True
)


from agno.team import Team

db_team = Team(
    name="db-team",
    model =model, 
    members=[
        schema_agent,
        query_agent,
        executor_agent
    ],
    db=SqliteDb(db_file="team.db"),
    instructions = [
            "You are a PostgreSQL database assistant chatbot.",
            "You MUST answer using the database.",
            "Before writing SQL, always check schema context using load_schema_knowledge().",
            "Only use tables and columns that exist in the schema context.",
            "If user asks for top/most/count/trends, generate SQL and execute using run_sql().",
            "If filtering by year/month/day, prefer timestamp columns like createdAt",
            "If the column values are null try to filter on other by observing the sampple data columns by conformation with the sample_knowledge"
            "If a time column is bigint, treat it as epoch milliseconds unless proven otherwise.",
            "Return final answer as it is the query returns",
    ],
    add_history_to_context=True,
    num_history_runs=3,
    add_team_history_to_members=True, 
    markdown=True
)

