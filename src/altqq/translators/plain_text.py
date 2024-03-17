"""Module for converting Query objects to plain text SQL."""

import dataclasses as dc
import typing
from typing import Any

from altqq.structs import Query
from altqq.types import QueryValueTypes, T
from typing_extensions import Annotated


class PlainTextTranslator:
    """Converts a `Query` to a plain text SQL."""

    def _resolve_value(self, query: Query, field: dc.Field[T]) -> Any:
        value = getattr(query, field.name)
        if field.type == Query:
            return self.__call__(value)

        if typing.get_origin(field.type) == Annotated:
            # Pyright can't match the __metadata__ attribute to Annotated
            if QueryValueTypes.NON_PARAMETER in field.type.__metadata__:  # type: ignore
                return value

        # Numeric types are not escaped
        if isinstance(value, (int, float)):
            return value

        # None is written as NULL
        if value is None:
            return "NULL"

        # All other types fall down to strings and are escaped
        return f"'{value}'"

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
