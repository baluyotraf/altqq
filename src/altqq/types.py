"""Module for typing related things."""

import enum
from typing import List, TypeVar

from typing_extensions import Annotated

T = TypeVar("T")


class QueryValueTypes(enum.Enum):
    """Defines the types of values `Query` can take."""

    PARAMETER = enum.auto()
    LIST_PARAMETER = enum.auto()
    NON_PARAMETER = enum.auto()


NonParameter = Annotated[T, QueryValueTypes.NON_PARAMETER]
ListParameter = Annotated[List[T], QueryValueTypes.LIST_PARAMETER]
