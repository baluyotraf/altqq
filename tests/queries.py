"""Defines the queries for testing."""

import dataclasses as dc
from typing import Any, Literal

import altqq


@dc.dataclass
class TestQuery:
    """Defines the conversion of query to different translations."""

    query: altqq.Query
    pyodbc: altqq.PyODBCQuery
    plain_text: str


class SelectTableByFilter(altqq.Query):
    """Test query that selects and filters a table."""

    __query__ = """
        SELECT * FROM "{table}"
        WHERE "{filter_column}" = {filter_value}
    """

    table: altqq.NonParameter[str]
    filter_column: altqq.NonParameter[str]
    filter_value: Any


class OrderQuery(altqq.Query):
    """Test query that orders a query."""

    __query__ = """
        SELECT * FROM ({subquery}) AS tbl
        ORDER BY "{order_column}" {order}
    """

    subquery: altqq.Query
    order_column: altqq.NonParameter[str]
    order: altqq.NonParameter[Literal["asc", "desc"]]


class UnionAllQuery(altqq.Query):
    """Test query that union all two queries."""

    __query__ = """
        SELECT * FROM ({query1}) AS tbl1
        UNION ALL
        SELECT * FROM ({query2}) AS tbl2
    """

    query1: altqq.Query
    query2: altqq.Query


TEST_DATA = [
    TestQuery(
        SelectTableByFilter("Users", "name", "arietta"),
        pyodbc=altqq.PyODBCQuery(
            query="""SELECT * FROM "Users" WHERE "name" = ?""", parameters=["arietta"]
        ),
        plain_text="""SELECT * FROM "Users" WHERE "name" = 'arietta'""",
    )
]
