from typing import ClassVar

import pydantic.dataclasses as dc

QUERY_ATTRIB = "__query__"


class QueryMeta(type):
    def _check_query_attribute(dataclass, dct):
        try:
            if isinstance(getattr(dataclass, QUERY_ATTRIB), str):
                return True
        except AttributeError:
            return QUERY_ATTRIB in dct["__annotations__"]

        return False

    def __new__(cls, name, bases, dct):
        dataclass = super().__new__(cls, name, bases, dct)
        if not cls._check_query_attribute(dataclass, dct):
            raise ValueError(f"A string {QUERY_ATTRIB} must be provided")
        return dc.dataclass(dataclass)


class Query(metaclass=QueryMeta):
    __query__: ClassVar[str]
