import enum
from typing import TypeVar

from typing_extensions import Annotated

T = TypeVar("T")


class QueryValueTypes(enum.Enum):
    PARAMETER = enum.auto()
    NON_PARAMETER = enum.auto()


NonParameter = Annotated[T, QueryValueTypes.NON_PARAMETER]
