import dataclasses as dc
from typing import Any

from altqq.structs import Query


class PlainTextTranslator:
    def _resolve_value(self, dataclass, field: dc.Field) -> Any:
        value = getattr(dataclass, field.name)
        if field.type == Query:
            return self.__call__(value)
        return value

    def __call__(self, query: Query) -> str:
        fields = dc.fields(query)
        format_dict = {f.name: self._resolve_value(query, f) for f in fields}
        return query.__query__.format(**format_dict)
