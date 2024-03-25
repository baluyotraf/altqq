"""Translator related functions not belonging to other areas."""

import typing
from typing import Any

from typing_extensions import Annotated

from altqq.structs import Query
from altqq.types import QueryValueTypes


def is_query_instance(value: Any) -> bool:
    """Checks if the value is a subclass of altqq.structs.Query.

    Args:
        value (Any): Object to check.

    Returns:
        bool: True if a subclass, else False.
    """
    return isinstance(value, Query)


def is_parameter(cls: type) -> bool:
    """Checks if a type is a parameter type.

    Args:
        cls (type): Type to check.

    Returns:
        bool: True if parameter, else False.
    """
    if typing.get_origin(cls) == Annotated:
        # Pyright can't match the __metadata__ attribute to Annotated
        if QueryValueTypes.NON_PARAMETER in cls.__metadata__:  # type: ignore
            return True

    return False
