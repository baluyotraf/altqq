"""Module for converting Query objects for PyODBC execution."""

import dataclasses as dc
import typing
from string import Formatter
from typing import Any, Iterable, List, Mapping, Sequence, Union

from altqq.structs import Query
from altqq.types import QueryValueTypes, T
from typing_extensions import Annotated


@dc.dataclass
class PyODBCStatement:
    """Represents a generated PyODBC statement."""

    statement: Any
    parameters: Iterable[Any]


@dc.dataclass
class PyODBCQuery:
    """Converted `Query` object for PyODBC usage."""

    query: str
    parameters: Iterable[Any]


class PyODBCFormatter(Formatter):
    """Converts `PyODBCStatement` objects to query string.

    Aside from converting the `PyODBCStatement`, this class also tracks the
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
        kwargs: Mapping[str, PyODBCStatement],
    ) -> Any:
        """Retrieves the value formatting values from the statement mapping.

        Args:
            key (Union[str, int]): Key found in the raw string. Always `str`.
            args (Sequence[Any]): Ordered arguments. Unused.
            kwargs (Mapping[str, PyODBCStatement]): Key mapping to the
                PyODBCStatements.

        Returns:
            Any: The statement value provided in the PyODBCStatement.
        """
        # The args section is never used
        assert isinstance(key, str)

        field = kwargs[key]
        self.parameter_values.extend(field.parameters)
        return field.statement


class PyODBCTranslator:
    """Converts a `Query` to its corresponding `PyODBCQuery` object."""

    def _resolve_value(self, query: Query, field: dc.Field[T]) -> PyODBCStatement:
        value = getattr(query, field.name)
        if field.type == Query:
            qq = self.__call__(value)
            return PyODBCStatement(qq.query, qq.parameters)

        if typing.get_origin(field.type) == Annotated:
            # Pyright can't match the __metadata__ attribute to Annotated
            if QueryValueTypes.NON_PARAMETER in field.type.__metadata__:  # type: ignore
                return PyODBCStatement(value, ())

        return PyODBCStatement("?", [value])

    def __call__(self, query: Query) -> PyODBCQuery:
        """Converts a `Query` to its corresponding `PyODBCQuery` object.

        Args:
        query (Query): Query to translate to PyODBC

        Returns:
            PyODBCQuery: Equivalent query for PyODBC usage.
        """
        formatter = PyODBCFormatter()
        fields = dc.fields(query)
        format_dict = {f.name: self._resolve_value(query, f) for f in fields}

        return PyODBCQuery(
            query=formatter.format(query.__query__, **format_dict),
            parameters=formatter.parameter_values,
        )
