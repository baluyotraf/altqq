import enum
from typing import ClassVar, Protocol, Annotated, TypeVar, Any
from altqq.structs import Query

_T = TypeVar("_T")

class QueryValueType(enum.Enum):
    PARAMETER = enum.auto()
    NON_PARAMETER = enum.auto()

NonParameter = Annotated[_T, QueryValueType.NON_PARAMETER]

class Translator(Protocol):
    def __call__(query: Query) -> Any:
        ...
