[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

# Alternative Queries

Alternative queries is a library created to help with handcrafted SQL queries.
It works by providing a class that represent the queries, with parameters type
checked by `Pydantic`.

The library is currently still in development and has an alpha release.

## Installation

The library is available in PyPI

```bash
pip install altqq
```

## Basic Usage

To use the library, you can define a class that represents a query. Then this
query can be converted to plain text or `pyodbc` usable query.

```python
import altqq

class SelectUserByFirstName(altqq.Query):
    __query__ = """
        SELECT * FROM "Users"
        WHERE first_name = {first_name}
    """
    first_name: str

q = altqq.to_pyodbc(SelectUserByFirstName(first_name="arietta"))
print(q.query)
print(q.parameters)
```

Running the code above should give the result below:

```bash

        SELECT * FROM "Users"
        WHERE first_name = ?

['arietta']
```

## Templating Non-Parameters

By default, the class properties are treated as parameters. If there's a need
for more customization, they can be declared as `altqq.NonParameter`.

```python
import altqq

class SelectByFirstName(altqq.Query):
    __query__ = """
        SELECT * FROM "{table}"
        WHERE first_name = {first_name}
    """
    first_name: str
    table: altqq.NonParameter[str]

q = altqq.to_pyodbc(SelectByFirstName(
    first_name="arietta",
    table="Users"
))
print(q.query)
print(q.parameters)
```

Running the code above should give the result below:

```bash

        SELECT * FROM "Users"
        WHERE first_name = ?

['arietta']
```

## Nested Queries

Queries can also use other queries. When passed to the functions for conversion,
other queries will also be converted.

```python
import altqq

class SelectUserByFirstName(altqq.Query):
    __query__ = """
        SELECT * FROM "Users"
        WHERE first_name = {first_name}
    """
    first_name: str


class SelectSubqueryByAge(altqq.Query):
    __query__ = """
        SELECT * FROM ({subquery}) AS tbl
        WHERE tbl.age = {age}
    """
    age: int
    subquery: altqq.Query

q = altqq.to_pyodbc(SelectSubqueryByAge(
    age=20,
    subquery=SelectUserByFirstName(
        first_name="arietta"
    )
))
print(q.query)
print(q.parameters)
```

Running the code above should give the result below:

```bash

        SELECT * FROM (
        SELECT * FROM "Users"
        WHERE first_name = ?
    ) AS tbl
        WHERE tbl.age = ?

['arietta', 20]
```

## Road Map

Below is the list of things planned for the library

- Documentation Page
- Tests
- Expansion of Supported Version
- Support for other Python Database Tooling
