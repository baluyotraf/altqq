"""Structures used for defining queries."""

from typing import Any, ClassVar, Dict, Tuple

import pydantic.dataclasses as dc
from typing_extensions import dataclass_transform

QUERY_ATTRIB = "__query__"


@dataclass_transform()
class QueryMeta(type):
    """Metaclass for generating Query objects that the library supports.

    Classes using this metaclass are automatically converted to Pydantic
    Dataclasses for validation support. Also, the `__query__` attribute is
    verified to be provided either as a value or as a type hint.

    Raises:
        ValueError: When the `__query__` attribute is not defined.

    Returns:
        _type_: A new type compatible for the library query functionalities.
    """

    @staticmethod
    def _check_query_attribute(dataclass: "QueryMeta", dct: Dict[str, Any]):
        try:
            if isinstance(getattr(dataclass, QUERY_ATTRIB), str):
                return True
        except AttributeError:
            return QUERY_ATTRIB in dct["__annotations__"]

        return False

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        """Creates a new class of the metaclass.

        This wraps the newly created class with Pydantic Dataclass and checks
        the `__query__` attribute.
        """
        dataclass = super().__new__(cls, name, bases, dct)
        if not cls._check_query_attribute(dataclass, dct):
            raise ValueError(f"A string {QUERY_ATTRIB} must be provided")
        return dc.dataclass(dataclass)


class Query(metaclass=QueryMeta):
    """Base class for query definitions.

    This class can be inherited instead of providing the `QueryMeta` as the
    class metaclass.
    """

    __query__: ClassVar[str]
