"""Tests the translations of queries."""

import altqq
import pytest

from tests.queries import TEST_DATA, SampleQuery
from tests.utils import clean_whitespaces as cws


@pytest.mark.parametrize("query", TEST_DATA)
def test_to_pyodbc__proper_query__correct_pyodbc_object(query: SampleQuery):
    """If the query parameters are correct, the pyodbc object is returned."""
    res = altqq.to_pyodbc(query.query)
    assert cws(query.pyodbc.query) == cws(res.query)
    assert query.pyodbc.parameters == res.parameters


@pytest.mark.parametrize("query", TEST_DATA)
def test_to_psycopg__proper_query__correct_sql(query: SampleQuery):
    """If the query parameters are correct, the psycopg object is returned."""
    res = altqq.to_psycopg(query.query)
    assert cws(query.psycopg.query) == cws(res.query)
    assert query.psycopg.parameters == res.parameters


@pytest.mark.parametrize("query", TEST_DATA)
def test_to_plain_text__proper_query__correct_sql(query: SampleQuery):
    """If the query parameters are correct, the sql is returned."""
    sql = altqq.to_plain_text(query.query)
    assert cws(query.plain_text) == cws(sql)
