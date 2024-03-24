# Why use Alternative Queries?

Arguments for ORM, Stored Procedures, handcrafted queries, and other methods of
managing your database interactions will `NOT` be the content of this section.
The assumption is you decided to work on writing handcrafted queries.

The content of this section is to present several ways in which Alternative
Queries can help you in your journey to writing nicer handcrafted queries.

## Typed Parameters

Typing has been added to python since version `3.5` and for good reason. Typing
reduces the space for errors when working with code. In the example below, there
are no clues as to what the `id` should be. Even the query context can not help
in this situation since database IDs can be `UUID`, `int`, or `str` type.

```python
my_query = """
    SELECT * FROM "Users" where id = {id}
"""
```

Using Alternative Queries allows definition of types with the query. It also
checks that all the parameters required by the query are provided. This means
that unlike a string query, one does not need to remember to call `format` every
time.

```python
import uuid
import altqq

class MyQuery(altqq.Query):
    __query__ = """
        SELECT * FROM "Users" where id = {id}
    """
    id: uuid.UUID

MyQuery(id=10) # Throws ValidationError
MyQuery() # Throws ValidationError
MyQuery(id=uuid.uuid4()) # Works perfectly

```

## Managing Ordered Parameters

Alternative Queries helps you in managing your query parameters. For example,
for ODBC databases, `pyodbc` does not allow named parameters. It means that to
reuse queries, one needs to make note of the parameters, as they must be in
order. For example:

```python
import uuid

my_query = """
    SELECT * from "Users" where "id" = ? and "name" = ?
"""
parameters = [uuid.uuid4(), "Arie"]
```

The Alternative Queries equivalent provides a named option to help manage the
parameters. These names are also suggested if one is using a Python IDE. This
also reduces redundancy if a query uses a parameter multiple times.

```python
import uuid
import altqq

class MyQuery(altqq.Query):
    __query__ = """
        SELECT * from "Users" where "id" = {id} and "name" = {name}
    """
    id: uuid.UUID
    name: str

# The order and parameter names are provided as suggestion by the IDE
MyQuery(id=uuid.uuid4(), name="Arie")
```

## Managing Named Parameters

`psycopg` and `mysql` supports named parameters. For these libraries,
Alternative Queries help in nested queries. Manually merging the query strings
can introduce name conflicts. On the other hand, Alternative Queries perform
substitution on a query basis, allowing name reuse. For example:

```python
query1 = """
    SELECT * from "Teachers" where "id" = %(id)s and "name" = %(name)s
"""
parameters1 = {"id": uuid.uuid4(), "name": "Arie"}

query2 = """
    SELECT * from "Students" where "id" = %(id)s and "name" = %(name)s
"""
parameters2 = {"id": uuid.uuid4(), "name": "Falsita"}

# query1 and query2 use the same parameter names
query3 = f"{query1} UNION ALL {query2}"
# this actually does not work since the same keys will overwrite values
parameters3 = {**parameters1, **parameters2}
```

Alternative Queries take the parameters together with their respective class.
This allows Alternative Queries to scope the names of the parameters being
provided. When working with `psycopg` and `mysql`, Alternative Queries will
still provide the parameters as a `tuple`, which means the names do not matter
to the final result.

```python
import uuid
import altqq

class Query1(altqq.Query):
    __query__ = """
        SELECT * from "Teachers" where "id" = {id} and "name" = {name}
    """
    id: uuid.UUID
    name: str

query1 = Query1(id=uuid.uuid4(), name="Arie")

class Query2(altqq.Query):
    __query__ = """
        SELECT * from "Students" where "id" = {id} and "name" = {name}
    """
    id: uuid.UUID
    name: str

query2 = Query2(id=uuid.uuid4(), name="Falsita")

class Query3(altqq.Query):
    __query__ = """
        {query1} UNION ALL {query2}
    """
    query1: altqq.Query
    query2: altqq.Query

query3 = Query3(query1=query1, query2=query2)

res = altqq.to_psycopg(query3)
print(res.parameters) # (UUID('...'), 'Arie', UUID('...'), 'Falsita')
```

## Nesting Queries

Alternative Queries help in reusing and nesting queries. One common example of a
reusable template is paging.

```python
def page_query(query, parameters, page, items_per_page):
    page = """
        SELECT * FROM ( {query} ) as base
        ...
    """
    return page_query, (*parameters, page, items_per_page)

page_query(my_query, my_parameters, page, items_per_page)
```

The Alternative Queries equivalent provides type checking during run-time, as
well as removing the logic for handling the parameter merging. Having ordered
parameters makes parameter merging easier. However, the lack of named parameters
can make defining parameters error-prone. Alternative Queries provide a named
option, while doing the parameter merging under the hood.

```python
import typing
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
