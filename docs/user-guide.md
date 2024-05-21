# User Guide

This is a more thorough guide on the functionalities of Alternative Queries.

As a general usage rule, rely on the objects provided by the `altqq` module.
Consider the internal modules in the `altqq.*` as highly unstable.

## Typed Queries

The most basic functionality of Alternative Queries is to provide types to the
query parameters.

```python
import altqq

class MyQuery(altqq.Query):
    __query__ = "..."

    parameter1: str
    parameter2: int
```

The types are checked using `Pydantic`, so the type casting rules that
`Pydantic` follow also applies. For more details, read the [Pydantic Types]
documentation.

[Pydantic Types]: https://docs.pydantic.dev/latest/concepts/types/

## Non-Parameter Substitution

Sometimes, there is a need to provide a value not as a parameter, but as an
actual value. A simple example of this is wanting a query to work on different
tables.

```python
import altqq

class MyQuery(altqq.Query):
    __query__ = """ SELECT * FROM "{table}" """
    table: altqq.NonParameter[str]

res = altqq.to_pyodbc(MyQuery("Users"))

print(res.query) #  SELECT * FROM "Users"
print(res.parameters) # []
```

These values must be defined using the `altqq.NonParameter` types. These types
of values must be defined explicitly, as they can introduce SQL injections if
used incorrectly.

## Nested Queries

To use a query inside a query, simply define the type of class attribute as
`altqq.Query`. This will merge all the parameters of the child queries to the
parent query.

```python
import altqq

class Paging(altqq.Query):
    __query__ = """
        SELECT * FROM ( {query} ) as base
        ...
    """
    query: altqq.Query

    page: int
    items_per_page: int

query = Paging(MyQuery(...), page, items_per_page)
```

## Calculated Values

There are cases in which one would prefer to compute the value of a parameter.
For example, defining the columns to fetch inside a `SELECT` query.

```python
import altqq

class Select(altqq.Query):
    __query__ = """
        SELECT {_columns} FROM "{table}"
    """
    table: altqq.NonParameter[str]
    columns: altqq.NonParameter[typing.Iterable[str]]

    _columns: altqq.NonParameter[str] = altqq.Calculated

    def __post_init__(self):
        # Convert ["a", "b", "c"] to "a","b","c"
        self._columns = ",".join(f'"{c}"'for c in self.columns)

query = Select(table="Users", columns=["id", "first_name", "last_name"])
res = altqq.to_pyodbc(query)
print(res.query) # SELECT "id","first_name","last_name" FROM "Users"
```

Assigning a value as `altqq.Calculated` means that the value will not be
provided by the user. Internally, `altqq.Calculated` is just replaced with
`dataclasses.field(init=False)`. Given that all `altqq.Query` objects are
`Pydantic` `dataclass`, the calculated values can be assigned inside the
`__post_init__` method.

As defined by the `Pydantic` `dataclass` behavior, the types for the assignment
inside the `__post_init__` method are not checked.

## List Parameters

For list that are used as parameters, a special `altqq.ListParameter` typing can
be used to denote that `altqq` should expand the list as a parameter.

```python
import altqq

class SelectUser(altqq.Query):
    __query__ = """
        SELECT * FROM Users WHERE user_id in {user_id}
    """

    user_id: altqq.ListParameter[int]


query = SelectUser(user_id=[1,2,3])
res = altqq.to_pyodbc(query)
print(res.query) # SELECT * FROM Users WHERE user_id in (?,?,?)
```

## Additional Validation

As `altqq.Query` objects are `Pydantic` `dataclass` internally, one can also
perform more rigid validation to the parameter values. For more details, read
the documentation on [Pydantic Dataclasses].

[Pydantic Dataclasses]: https://docs.pydantic.dev/latest/concepts/dataclasses/
