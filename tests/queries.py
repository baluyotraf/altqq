"""Defines the queries for testing."""

import dataclasses as dc
from typing import Any, Literal

import altqq


@dc.dataclass
class SampleQuery:
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
        SELECT * FROM ( {subquery} ) AS tbl
        ORDER BY "{order_column}" {order}
    """

    subquery: altqq.Query
    order_column: altqq.NonParameter[str]
    order: altqq.NonParameter[Literal["asc", "desc"]]


class UnionAllQuery(altqq.Query):
    """Test query that union all two queries."""

    __query__ = """
        SELECT * FROM ( {query1} ) AS tbl1
        UNION ALL
        SELECT * FROM ( {query2} ) AS tbl2
    """

    query1: altqq.Query
    query2: altqq.Query


TEST_DATA = [
    SampleQuery(
        SelectTableByFilter("Users", "age", 25),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT * FROM "Users" WHERE "age" = ?
            """,
            parameters=[25],
        ),
        plain_text="""
            SELECT * FROM "Users" WHERE "age" = 25
        """,
    ),
    SampleQuery(
        OrderQuery(SelectTableByFilter("Users", "last_name", "Fine"), "age", "asc"),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT * FROM (
                    SELECT * FROM "Users" WHERE "last_name" = ?
                ) AS tbl
                ORDER BY "age" asc
            """,
            parameters=["Fine"],
        ),
        plain_text="""
            SELECT * FROM (
                SELECT * FROM "Users" WHERE "last_name" = 'Fine'
            ) AS tbl
            ORDER BY "age" asc
        """,
    ),
    SampleQuery(
        UnionAllQuery(
            SelectTableByFilter("Music", "title", "Secret"),
            SelectTableByFilter("Cities", "name", "Piova"),
        ),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT * FROM (
                    SELECT * FROM "Music" WHERE "title" = ?
                ) AS tbl1
                UNION ALL
                SELECT * FROM (
                    SELECT * FROM "Cities" WHERE "name" = ?
                ) AS tbl2
            """,
            parameters=["Secret", "Piova"],
        ),
        plain_text="""
            SELECT * FROM (
                SELECT * FROM "Music" WHERE "title" = 'Secret'
            ) AS tbl1
            UNION ALL
            SELECT * FROM (
                SELECT * FROM "Cities" WHERE "name" = 'Piova'
            ) AS tbl2
        """,
    ),
]
