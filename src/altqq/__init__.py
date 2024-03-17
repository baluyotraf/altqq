from altqq.translators.pyodbc import PyODBCTranslator
from altqq.structs import Query
from altqq.types import NonParameter

from typing import Tuple, Any

PYODBC = PyODBCTranslator()

def to_pyodbc(query: Query) -> Tuple[str, Tuple[Any, ...]]:
    return PYODBC(query)
