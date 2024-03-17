import enum
from typing import Annotated, TypeVar

_T = TypeVar("_T")


class QueryValueTypes(enum.Enum):
    PARAMETER = enum.auto()
    NON_PARAMETER = enum.auto()


NonParameter = Annotated[_T, QueryValueTypes.NON_PARAMETER]
