"""Translator related functions not belonging to other areas."""

import typing

from typing_extensions import Annotated

from altqq.structs import Query
from altqq.types import QueryValueTypes


def is_query_subclass(cls: type) -> bool:
    """Checks if the type is a subclass of altqq.structs.Query.

    Args:
        cls (type): Type to check.

    Returns:
        bool: True if a subclass, else False.
    """
    try:
        return issubclass(cls, Query)
    except TypeError:
        pass

    return False


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
