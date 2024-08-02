"""Module for converting Query objects to plain text SQL."""

import dataclasses as dc
from typing import Any

from altqq.structs import Query
from altqq.translators import common
from altqq.types import QueryValueTypes, T


class PlainTextTranslator:
    """Converts a `Query` to a plain text SQL."""

    def _resolve_parameters(self, value: Any) -> str:
        # Numeric types are not escaped
        if isinstance(value, (int, float)):
            return str(value)

        # None is written as NULL
        if value is None:
            return "NULL"

        # All other types fall down to strings and are escaped
        return f"'{value}'"

    def _resolve_value(self, query: Query, field: dc.Field[T]) -> str:
        value = getattr(query, field.name)
        if common.is_query_instance(value):
            return self.__call__(value)

        # Field has no typing in older python versions
        field_type = common.get_parameter_type(field.type)  # type: ignore
        if field_type == QueryValueTypes.NON_PARAMETER:
            return value
        elif field_type == QueryValueTypes.LIST_PARAMETER:
            comma_separated = ",".join(self._resolve_parameters(p) for p in value)
            return f"({comma_separated})"
        else:
            return self._resolve_parameters(value)

    def __call__(self, query: Query) -> str:
        """Converts a `Query` to a plain text SQL.

        The conversion to plain text also handles some of the data types. None
        is converted to `NULL`, numeric values are written as they are and
        string values and other object types are escaped using `'`.

        Args:
            query (Query): Query to convert.

        Returns:
            str: Query as plain text.
        """
        fields = dc.fields(query)
        format_dict = {f.name: self._resolve_value(query, f) for f in fields}
        return query.__query__.format(**format_dict)
