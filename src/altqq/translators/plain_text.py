from string import Formatter
import dataclasses as dc

from altqq.structs import Query
from altqq.types import QueryValueTypes
from typing import Tuple, Iterable, Any, Annotated, Mapping
import typing

class PlainTextTranslator:

    def _resolve_value(self, dataclass, field: dc.Field) -> Any:
        value = getattr(dataclass, field.name)
        if field.type == Query:
            return self.__call__(value)
        return value

    def __call__(self, query: Query) -> str:
        fields = dc.fields(query)
        format_dict = {
            f.name: self._resolve_value(query, f)
            for f in fields
        }
        return query.__query__.format(**format_dict)
    