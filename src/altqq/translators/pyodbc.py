import dataclasses as dc
import typing
from string import Formatter
from typing import Any, Iterable, List, Mapping, Sequence, Tuple, Union

from altqq.structs import Query
from altqq.types import QueryValueTypes, T
from typing_extensions import Annotated


@dc.dataclass
class PyODBCStatement:
    statement: Any
    parameters: Iterable[Any]


class PyODBCFormatter(Formatter):
    def __init__(self):
        self.reset()

    def reset(self):
        self.parameter_values: List[Any] = []

    def get_value(
        self,
        key: Union[str, int],
        args: Sequence[Any],
        kwargs: Mapping[str, PyODBCStatement],
    ) -> Any:
        # The args section is never used
        assert isinstance(key, str)

        field = kwargs[key]
        self.parameter_values.extend(field.parameters)
        return field.statement


class PyODBCTranslator:
    def _resolve_value(self, query: Query, field: dc.Field[T]) -> PyODBCStatement:
        value = getattr(query, field.name)
        if field.type == Query:
            query_string, query_params = self.__call__(value)
            return PyODBCStatement(query_string, query_params)

        if typing.get_origin(field.type) == Annotated:
            # Pyright can't match the __metadata__ attribute to Annotated
            if QueryValueTypes.NON_PARAMETER in field.type.__metadata__:  # type: ignore
                return PyODBCStatement(value, ())

        return PyODBCStatement("?", [value])

    def __call__(self, query: Query) -> Tuple[str, Tuple[Any, ...]]:
        formatter = PyODBCFormatter()
        fields = dc.fields(query)
        format_dict = {f.name: self._resolve_value(query, f) for f in fields}

        query_string = formatter.format(query.__query__, **format_dict)
        query_params = formatter.parameter_values
        return query_string, tuple(query_params)
