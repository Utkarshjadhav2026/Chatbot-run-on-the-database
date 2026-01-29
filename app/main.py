from agno_agent1 import agent
from agno.utils.pprint import pprint_run_response

while True:
    q = input("\nAsk DB Question (or exit): ")
    if q.lower() == "exit":
        break

    response = agent.run(q)
    pprint_run_response(response, markdown=True)



# from agno_agent1 import db_team
# from schema import AgentResponse, TableRow, TableResult

# while True:
#     q = input("Ask DB Question (or exit): ")
#     if q.lower() == "exit":
#         break

#     response = db_team.run(q)

#     sql = response.tool_calls[0].args["query"]
#     result = response.tool_results[0]

#     table = TableResult(
#         columns=result["columns"],
#         rows=[TableRow(values=r) for r in result["rows"]],
#     )

#     final = AgentResponse(
#         question=q,
#         sql=sql,
#         result=table
#     )

#     print(final.model_dump_json(indent=2))
