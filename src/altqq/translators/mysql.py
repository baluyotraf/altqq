"""Module for converting Query objects for mysql execution."""

# For now the psycopg classes are being reused for mysql since they use
# similar formatting. This can changed if there are edge cases that were
# missed so separate classes will be introduced for it

import dataclasses as dc
from typing import Any, Tuple

from altqq.structs import Query
from altqq.translators.psycopg import PsycopgTranslator


@dc.dataclass
class MySQLQuery:
    """Converted `Query` object for MySQL usage."""

    query: str
    parameters: Tuple[Any, ...]


class MySQLTranslator:
    """Converts a `Query` to its corresponding `MySQLQuery` object."""

    def __init__(self):
        self._translator = PsycopgTranslator()

    def __call__(self, query: Query) -> MySQLQuery:
        """Converts a `Query` to its corresponding `MySQL` object.

        Args:
            query (Query): Query to translate to MySQL

        Returns:
            MySQLQuery: Equivalent query for MySQL usage.
        """
        psql_query = self._translator(query)
        return MySQLQuery(query=psql_query.query, parameters=psql_query.parameters)
