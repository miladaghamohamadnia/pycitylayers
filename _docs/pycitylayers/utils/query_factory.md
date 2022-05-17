# Query Factory

> Auto-generated documentation for [pycitylayers.utils.query_factory](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/utils/query_factory.py) module.

- [Pycitylayers](../../README.md#pycitylayers) / [Modules](../../MODULES.md#pycitylayers-modules) / [Pycitylayers](../index.md#pycitylayers) / [Utils](index.md#utils) / Query Factory
    - [query_gql_all_columns](#query_gql_all_columns)
    - [query_gql_all_tables](#query_gql_all_tables)
    - [query_gql_rows](#query_gql_rows)

## query_gql_all_columns

[[find in source code]](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/utils/query_factory.py#L12)

```python
def query_gql_all_columns(table_name):
```

## query_gql_all_tables

[[find in source code]](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/utils/query_factory.py#L6)

```python
def query_gql_all_tables():
```

## query_gql_rows

[[find in source code]](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/utils/query_factory.py#L19)

```python
def query_gql_rows(
    table='',
    columns=[],
    nrows=5,
    skiprows=0,
    geometry=None,
    geometry_operation='is_within_poly',
    **kwargs,
):
```
