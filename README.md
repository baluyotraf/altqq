[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![qa](https://github.com/baluyotraf/altqq/actions/workflows/qa.yml/badge.svg)](https://github.com/baluyotraf/altqq/actions/workflows/qa.yml)
[![release](https://github.com/baluyotraf/altqq/actions/workflows/release.yml/badge.svg)](https://github.com/baluyotraf/altqq/actions/workflows/release.yml)

# Alternative Queries

Alternative queries is a library created to help with handcrafted SQL queries.
It works by providing a class that represent the queries where its parameter
types are checked by `Pydantic`.

If you want to write reusable and nested handcrafted SQL queries, you can check
more information on the [Alternative Queries Documentation]. If you want to know
how Alternative Queries can help you, check the [Why use Alternative Queries?]
section of the documentation.

[Alternative Queries Documentation]: https://altqq.baluyotraf.com/stable/
[Why use Alternative Queries?]: https://altqq.baluyotraf.com/stable/rationale/

## Installation

The library is available in the Python Package Index.

```bash
pip install altqq
```

## Quick Start

To start, define a class by inheriting the `altqq.Query` class. The class should
have a query following the python formatting standards. The variable names
inside the `__query__` must match the other attributes defined on the class.

```python
import altqq

class SelectUserByFirstName(altqq.Query):
    __query__ = """
        SELECT * FROM "Users"
        WHERE first_name = {first_name}
    """
    first_name: str
```

The class can be used like a `dataclass`. In fact, classes inheriting the
`altqq.Query` class are turned into a `Pydantic` `dataclass`.

```python
query = SelectUserByFirstName(first_name="arietta")
```

The object can be converted into a query suitable for a DBMS library of your
choice. For example, calling the `altqq.to_pyodbc` function will convert the
object to `PyODBCQuery` which provides the query string and the parameters.

```python
pyodbc_query = altqq.to_pyodbc(query)
print(pyodbc_query.query)
#
#        SELECT * FROM "Users"
#        WHERE first_name = ?
#
print(pyodbc_query.parameters)
# ['arietta']
```
