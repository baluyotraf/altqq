"""Tests the translations of queries."""

from typing import ClassVar

import altqq
import pytest


def test_query_subclass__no_annotations__raises_error():
    """If subclass does not have any annotations, raise a ValueError."""
    with pytest.raises(ValueError):

        class _(altqq.Query):
            pass


def test_query_subclass__without__query__raises_error():
    """If subclass has annotations, but no __query__, raise a ValueError."""
    with pytest.raises(ValueError):

        class _(altqq.Query):
            props: int


def test_query_subclass__query_defined__works():
    """If subclass defines __query__ attribute, all is good."""

    class _(altqq.Query):
        __query__ = "My query"


def test_query_subclass__query_typed__works():
    """If subclass defines __query__ with a type hint, all is good."""

    class _(altqq.Query):
        __query__: ClassVar[str]
