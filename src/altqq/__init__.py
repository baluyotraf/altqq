from typing import Any, Tuple

from altqq.structs import Query
from altqq.translators.plain_text import PlainTextTranslator
from altqq.translators.pyodbc import PyODBCTranslator
from altqq.types import NonParameter as NonParameter


class Translators:
    PYODBC = PyODBCTranslator()
    PLAIN_TEXT = PlainTextTranslator()


def to_pyodbc(query: Query) -> Tuple[str, Tuple[Any, ...]]:
    return Translators.PYODBC(query)


def to_plain_text(query: Query) -> str:
    return Translators.PLAIN_TEXT(query)
