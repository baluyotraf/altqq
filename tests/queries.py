"""Defines the queries for testing."""

import dataclasses as dc
from typing import Any, Literal

import altqq


@dc.dataclass
class SampleQuery:
    """Defines the conversion of query to different translations."""

    query: altqq.Query
    pyodbc: altqq.PyODBCQuery
    psycopg: altqq.PsycopgQuery
    plain_text: str

    @property
    def mysql(self) -> altqq.MySQLQuery:
        """Generates mysql query from psycopg."""
        return altqq.MySQLQuery(
            query=self.psycopg.query, parameters=self.psycopg.parameters
        )


class SelectWithCalculated(altqq.Query):
    """Test queries that uses multiple calculated values."""

    __query__ = """
        SELECT * FROM Table WHERE A = {param} AND B = {calc1} AND C = {calc2}
    """

    param: int
    calc1: int = altqq.Calculated
    calc2: int = altqq.Calculated

    def __post_init__(self):
        """Initialize calculated parameters."""
        self.calc1 = 20
        self.calc2 = 30


class SelectWithList(altqq.Query):
    """Test query that uses a list."""

    __query__ = """
        SELECT * FROM table WHERE A IN {list}
    """

    list: altqq.ListParameter[int]


class SelectTableByFilter(altqq.Query):
    """Test query that selects and filters a table."""

    __query__ = """
        SELECT *, (15 % 10) AS t FROM "{table}"
        WHERE "{filter_column}" = {filter_value}
    """

    table: altqq.NonParameter[str]
    filter_column: altqq.NonParameter[str]
    filter_value: Any


class SelectTableByFilterNonParameter(altqq.Query):
    """Test query that selects and filters a table."""

    __query__ = """
        SELECT *, (15 % 10) AS t FROM "{table}"
        WHERE "{filter_column}" = {filter_value}
    """

    table: altqq.NonParameter[str]
    filter_column: altqq.NonParameter[str]
    filter_value: altqq.NonParameter[int]


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

    query1: SelectTableByFilter
    query2: SelectTableByFilter


TEST_DATA = [
    SampleQuery(
        SelectWithCalculated(10),
        pyodbc=altqq.PyODBCQuery(
            query="""SELECT * FROM Table WHERE A = ? AND B = ? AND C = ?""",
            parameters=[10, 20, 30],
        ),
        psycopg=altqq.PsycopgQuery(
            query="""SELECT * FROM Table WHERE A = %s AND B = %s AND C = %s""",
            parameters=(10, 20, 30),
        ),
        plain_text="""SELECT * FROM Table WHERE A = 10 AND B = 20 AND C = 30""",
    ),
    SampleQuery(
        SelectWithList([10, 20, 30]),
        pyodbc=altqq.PyODBCQuery(
            query="""SELECT * FROM table WHERE A IN (?,?,?)""", parameters=[10, 20, 30]
        ),
        psycopg=altqq.PsycopgQuery(
            query="""SELECT * FROM table WHERE A IN (%s,%s,%s)""",
            parameters=(10, 20, 30),
        ),
        plain_text="""SELECT * FROM table WHERE A IN (10,20,30)""",
    ),
    SampleQuery(
        SelectTableByFilterNonParameter("Users", "age", 25),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT *, (15 % 10) AS t FROM "Users" WHERE "age" = 25
            """,
            parameters=[],
        ),
        psycopg=altqq.PsycopgQuery(
            query="""
                SELECT *, (15 % 10) AS t FROM "Users" WHERE "age" = 25
            """,
            parameters=(),
        ),
        plain_text="""
            SELECT *, (15 % 10) AS t FROM "Users" WHERE "age" = 25
        """,
    ),
    SampleQuery(
        SelectTableByFilter("Users", "age", 25),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT *, (15 % 10) AS t FROM "Users" WHERE "age" = ?
            """,
            parameters=[25],
        ),
        psycopg=altqq.PsycopgQuery(
            query="""
                SELECT *, (15 %% 10) AS t FROM "Users" WHERE "age" = %s
            """,
            parameters=(25,),
        ),
        plain_text="""
            SELECT *, (15 % 10) AS t FROM "Users" WHERE "age" = 25
        """,
    ),
    SampleQuery(
        OrderQuery(SelectTableByFilter("Users", "last_name", "Fine"), "age", "asc"),
        pyodbc=altqq.PyODBCQuery(
            query="""
                SELECT * FROM (
                    SELECT *, (15 % 10) AS t FROM "Users" WHERE "last_name" = ?
                ) AS tbl
                ORDER BY "age" asc
            """,
            parameters=["Fine"],
        ),
        psycopg=altqq.PsycopgQuery(
            query="""
                SELECT * FROM (
                    SELECT *, (15 %% 10) AS t FROM "Users" WHERE "last_name" = %s
                ) AS tbl
                ORDER BY "age" asc
            """,
            parameters=("Fine",),
        ),
        plain_text="""
            SELECT * FROM (
                SELECT *, (15 % 10) AS t FROM "Users" WHERE "last_name" = 'Fine'
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
                    SELECT *, (15 % 10) AS t FROM "Music" WHERE "title" = ?
                ) AS tbl1
                UNION ALL
                SELECT * FROM (
                    SELECT *, (15 % 10) AS t FROM "Cities" WHERE "name" = ?
                ) AS tbl2
            """,
            parameters=["Secret", "Piova"],
        ),
        psycopg=altqq.PsycopgQuery(
            query="""
                SELECT * FROM (
                    SELECT *, (15 %% 10) AS t FROM "Music" WHERE "title" = %s
                ) AS tbl1
                UNION ALL
                SELECT * FROM (
                    SELECT *, (15 %% 10) AS t FROM "Cities" WHERE "name" = %s
                ) AS tbl2
            """,
            parameters=("Secret", "Piova"),
        ),
        plain_text="""
            SELECT * FROM (
                SELECT *, (15 % 10) AS t FROM "Music" WHERE "title" = 'Secret'
            ) AS tbl1
            UNION ALL
            SELECT * FROM (
                SELECT *, (15 % 10) AS t FROM "Cities" WHERE "name" = 'Piova'
            ) AS tbl2
        """,
    ),
]
