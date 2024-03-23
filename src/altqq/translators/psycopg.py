"""Module for converting Query objects for Psycopg execution."""

import dataclasses as dc
import typing
from string import Formatter
from typing import Any, Iterable, List, Mapping, Sequence, Tuple, Union

from typing_extensions import Annotated

from altqq.structs import Query
from altqq.types import QueryValueTypes, T


@dc.dataclass
class PsycopgStatement:
    """Represents a generated Psycopg statement."""

    statement: Any
    parameters: Iterable[Any]


@dc.dataclass
class PsycopgQuery:
    """Converted `Query` object for Psycopg usage."""

    query: str
    parameters: Tuple[Any, ...]


class PsycopgFormatter(Formatter):
    """Converts `PsycopgStatement` objects to query string.

    Aside from converting the `PsycopgStatement`, this class also tracks the
    parameter substitutions during the formatting. These values are stored
    in the `parameter_values` attribute.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the state of the formatter."""
        self.parameter_values: List[Any] = []

    def get_value(
        self,
        key: Union[str, int],
        args: Sequence[Any],
        kwargs: Mapping[str, PsycopgStatement],
    ) -> Any:
        """Retrieves the value formatting values from the statement mapping.

        Args:
            key (Union[str, int]): Key found in the raw string. Always `str`.
            args (Sequence[Any]): Ordered arguments. Unused.
            kwargs (Mapping[str, PsycopgStatement]): Key mapping to the
                PsycopgStatements.

        Returns:
            Any: The statement value provided in the PsycopgStatement.
        """
        # The args section is never used
        assert isinstance(key, str)

        field = kwargs[key]
        self.parameter_values.extend(field.parameters)
        return field.statement


class PsycopgTranslator:
    """Converts a `Query` to its corresponding `PsycopgQuery` object."""

    def _resolve_value(self, query: Query, field: dc.Field[T]) -> PsycopgStatement:
        value = getattr(query, field.name)
        if field.type == Query:
            qq = self._convert_query(query)
            return PsycopgStatement(qq.query, qq.parameters)

        if typing.get_origin(field.type) == Annotated:
            # Pyright can't match the __metadata__ attribute to Annotated
            if QueryValueTypes.NON_PARAMETER in field.type.__metadata__:  # type: ignore
                return PsycopgStatement(value.replace("%", "%%"), ())

        return PsycopgStatement("%s", (value,))

    def _convert_query(self, query: Query) -> PsycopgQuery:
        formatter = PsycopgFormatter()
        fields = dc.fields(query)
        format_dict = {f.name: self._resolve_value(query, f) for f in fields}

        return PsycopgQuery(
            query=formatter.format(query.__query__.replace("%", "%%"), **format_dict),
            parameters=tuple(formatter.parameter_values),
        )

    def __call__(self, query: Query) -> PsycopgQuery:
        """Converts a `Query` to its corresponding `PsycopgQuery` object.

        Args:
            query (Query): Query to translate to Psycopg

        Returns:
            PsycopgQuery: Equivalent query for Psycopg usage.
        """
        psql_query = self._convert_query(query)
        if len(psql_query.parameters) == 0:
            psql_query.query = psql_query.query.replace("%%", "%")
        return psql_query