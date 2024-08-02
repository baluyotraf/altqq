"""Translator related functions not belonging to other areas."""

import typing
from typing import Any, Set, Type, cast

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


ANNOTATED_TYPES: Set[QueryValueTypes] = {
    QueryValueTypes.NON_PARAMETER,
    QueryValueTypes.LIST_PARAMETER,
}


def get_parameter_type(cls: Type[Any]) -> QueryValueTypes:
    """Extracts the value type based on the typing.

    Args:
        cls (Type[Any]): Type to check.

    Returns:
        QueryValueTypes: Role of the value in the query
    """
    if typing.get_origin(cls) == Annotated:
        # Pyright can't match the __metadata__ attribute to Annotated
        for metadata in cls.__metadata__:  # type: ignore
            if metadata in ANNOTATED_TYPES:
                return cast(QueryValueTypes, metadata)

    return QueryValueTypes.PARAMETER


def create_list_markers(marker: str, n: int) -> str:
    """Creates list markers for list parameter types.

    Args:
        marker (str): Parameter marker used by the translation
        n (int): Number of parameters in the list

    Returns:
        str: String to represent the list
    """
    comma_separated = ",".join(marker for _ in range(n))
    return f"({comma_separated})"
