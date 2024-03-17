from typing import Any, ClassVar, Dict, Tuple

import pydantic.dataclasses as dc
from typing_extensions import dataclass_transform

QUERY_ATTRIB = "__query__"


@dataclass_transform()
class QueryMeta(type):
    @staticmethod
    def _check_query_attribute(dataclass: "QueryMeta", dct: Dict[str, Any]):
        try:
            if isinstance(getattr(dataclass, QUERY_ATTRIB), str):
                return True
        except AttributeError:
            return QUERY_ATTRIB in dct["__annotations__"]

        return False

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        dataclass = super().__new__(cls, name, bases, dct)
        if not cls._check_query_attribute(dataclass, dct):
            raise ValueError(f"A string {QUERY_ATTRIB} must be provided")
        return dc.dataclass(dataclass)


class Query(metaclass=QueryMeta):
    __query__: ClassVar[str]
