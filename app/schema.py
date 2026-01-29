from pydantic import BaseModel
from typing import List, Any

class TableRow(BaseModel):
    values: List[Any]

class TableResult(BaseModel):
    columns: List[str]
    rows: List[TableRow]

class AgentResponse(BaseModel):
    question: str
    sql: str
    result: TableResult
