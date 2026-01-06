"""Structures used for defining queries."""

import dataclasses as dc
from typing import Any, ClassVar, Dict, Tuple

import pydantic.dataclasses as pdc
from pydantic import ConfigDict
from typing_extensions import dataclass_transform, get_annotations

QUERY_ATTRIB = "__query__"


class _Calculated:
    """Marker class for calculated values."""


# Typehint the class marker to Any to avoid conflict with the type checkers
Calculated: Any = _Calculated


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
    def _check_query_attribute(dataclass: "QueryMeta"):
        try:
            if isinstance(getattr(dataclass, QUERY_ATTRIB), str):
                return True
        except AttributeError:
            annotations = get_annotations(dataclass)
            return QUERY_ATTRIB in annotations

        return False

    @staticmethod
    def _resolve_calculated_fields(dct: Dict[str, Any]):
        for k, v in dct.items():
            if v == Calculated:
                dct[k] = dc.field(init=False)

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        """Creates a new class of the metaclass.

        This wraps the newly created class with Pydantic Dataclass and checks
        the `__query__` attribute.
        """
        cls._resolve_calculated_fields(dct)
        dataclass = super().__new__(cls, name, bases, dct)
        if not cls._check_query_attribute(dataclass):
            raise ValueError(f"A {QUERY_ATTRIB} value or type hint must be provided.")
        return pdc.dataclass(dataclass, config=ConfigDict(arbitrary_types_allowed=True))


class Query(metaclass=QueryMeta):
    """Base class for query definitions.

    This class can be inherited instead of providing the `QueryMeta` as the
    class metaclass.
    """

    __query__: ClassVar[str]
