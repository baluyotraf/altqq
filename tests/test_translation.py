"""Tests the translations of queries."""

import altqq
import pytest

from tests.queries import TEST_DATA, TestQuery
from tests.utils import clean_whitespaces as cws


@pytest.mark.parametrize("test_query", TEST_DATA)
def test_to_pyodbc__proper_query__correct_pyodbc_object(test_query: TestQuery):
    """If the query parameters are correct, the pyodbc object is returned."""
    res = altqq.to_pyodbc(test_query.query)
    assert cws(test_query.pyodbc.query) == cws(res.query)
    assert test_query.pyodbc.parameters == res.parameters


@pytest.mark.parametrize("test_query", TEST_DATA)
def test_to_plain_text__proper_query__correct_sqlt(test_query: TestQuery):
    """If the query parameters are correct, the sql is returned."""
    sql = altqq.to_plain_text(test_query.query)
    assert cws(test_query.plain_text) == cws(sql)
