# Query

> Auto-generated documentation for [pycitylayers.query.query](../../../pycitylayers/query/query.py) module.

Query classes for querying of DB

- [Pycitylayers](../../README.md#pycitylayers) / [Modules](../../MODULES.md#pycitylayers-modules) / [Pycitylayers](../index.md#pycitylayers) / [Query](index.md#query) / Query
    - [Query](#query)
        - [Query().url](#queryurl)
        - [Query().url](#queryurl)
    - [QueryCKAN](#queryckan)
    - [QueryGQL](#querygql)
        - [QueryGQL().get_all_tables](#querygqlget_all_tables)
        - [QueryGQL().get_columns](#querygqlget_columns)
        - [QueryGQL().get_rows](#querygqlget_rows)

## Query

[[find in source code]](../../../pycitylayers/query/query.py#L25)

```python
class Query():
    def __init__(*args, **kwargs):
```

Base Query class

### Query().url

[[find in source code]](../../../pycitylayers/query/query.py#L47)

```python
@property
def url():
```

property method to get current url of DB api

#### Returns

url string
Type: *string*

### Query().url

[[find in source code]](../../../pycitylayers/query/query.py#L57)

```python
@url.setter
def url(url):
```

method to set current url of DB api

#### Arguments

- `url` - url of DB api
:type url: string

## QueryCKAN

[[find in source code]](../../../pycitylayers/query/query.py#L84)

```python
class QueryCKAN(Query):
    def __init__(*args, **kwargs):
```

CKAN Querying class

#### See also

- [Query](#query)

## QueryGQL

[[find in source code]](../../../pycitylayers/query/query.py#L92)

```python
class QueryGQL(Query):
    def __init__(*args, **kwargs):
```

GraphQL Querying class

#### See also

- [Query](#query)

### QueryGQL().get_all_tables

[[find in source code]](../../../pycitylayers/query/query.py#L99)

```python
def get_all_tables():
```

### QueryGQL().get_columns

[[find in source code]](../../../pycitylayers/query/query.py#L108)

```python
def get_columns(table=''):
```

### QueryGQL().get_rows

[[find in source code]](../../../pycitylayers/query/query.py#L120)

```python
def get_rows(**kwargs):
```
