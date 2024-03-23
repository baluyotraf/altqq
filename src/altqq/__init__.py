"""Main entry point for the altqq library."""

from altqq.structs import Calculated as Calculated
from altqq.structs import Query
from altqq.translators.plain_text import PlainTextTranslator
from altqq.translators.psycopg import PsycopgQuery, PsycopgTranslator
from altqq.translators.pyodbc import PyODBCQuery, PyODBCTranslator
from altqq.types import NonParameter as NonParameter


class Translators:
    """Definition of available translators."""

    PYODBC = PyODBCTranslator()
    PSYCOPG = PsycopgTranslator()
    PLAIN_TEXT = PlainTextTranslator()


def to_pyodbc(query: Query) -> PyODBCQuery:
    """Converts a `Query` to its corresponding `PyODBCQuery` object.

    Args:
        query (Query): Query to translate to PyODBC

    Returns:
        PyODBCQuery: Equivalent query for PyODBC usage.
    """
    return Translators.PYODBC(query)


def to_psycopg(query: Query) -> PsycopgQuery:
    """Converts a `Query` to its corresponding `PsycopgQuery` object.

    Args:
        query (Query): Query to translate to Psycopg

    Returns:
        PsycopgQuery: Equivalent query for Psycopg usage.
    """
    return Translators.PSYCOPG(query)


def to_plain_text(query: Query) -> str:
    """Converts a `Query` to a plain text SQL.

    The conversion to plain text also handles some of the data types. None
    is converted to `NULL`, numeric values are written as they are and
    string values and other object types are escaped using `'`.

    Args:
        query (Query): Query to convert.

    Returns:
        str: Query as plain text.
    """
    return Translators.PLAIN_TEXT(query)
