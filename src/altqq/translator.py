from string import Formatter
import dataclasses as dc

from altqq.typing import Translator, Query, QueryValueType
from typing import Tuple, Iterable, Any, Annotated, Mapping
import typing

@dc.dataclass
class PyODBCValue:
    value: Any
    is_parameter: bool


class PyODBCFormatter(Formatter):

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.parameter_values = []
        
    def get_value(self, key: str, args: Tuple[()], kwargs: Mapping[str, PyODBCValue]) -> Any:
        field = kwargs[key]
        if field.is_parameter:
            self.parameter_values.append(field.value)
            return "?"
        else:
            return field.value

class PyODBCTranslator(Translator):

    def _resolve_value(self, dataclass, field: dc.Field) -> PyODBCValue:
        value = getattr(dataclass, field.name)
        if typing.get_origin(field.type) == Annotated:
            if QueryValueType.NON_PARAMETER in field.type.__metadata__:
                return PyODBCValue(value, False)
            
        return PyODBCValue(value, True)

    def __call__(self, query: Query) -> Tuple[str, Iterable[Any]]:
        formatter = PyODBCFormatter()
        fields = dc.fields(query)
        format_dict = {
            f.name: self._resolve_value(query, f)
            for f in fields
        }

        query_string = formatter.format(query.__query__, **format_dict)
        query_params = formatter.parameter_values
        return query_string, query_params

