# Client

> Auto-generated documentation for [pycitylayers.client.client](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/client/client.py) module.

Client class facilitating querying of DB

- [Pycitylayers](../../README.md#pycitylayers) / [Modules](../../MODULES.md#pycitylayers-modules) / [Pycitylayers](../index.md#pycitylayers) / [Client](index.md#client) / Client
    - [Client](#client)
        - [Client.create](#clientcreate)

## Client

[[find in source code]](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/client/client.py#L22)

```python
class Client():
    def __init__():
```

### Client.create

[[find in source code]](https://github.com/miladaghamohamadnia/pycitylayers/blob/main/pycitylayers/client/client.py#L26)

```python
@staticmethod
def create(*args, **kwargs):
```

Factory method instantiating appropriate query class
all valuse passed to this function is passed down to corresponding class initialization

#### Arguments

- `source` - source DB name based on their categories
:type source: string

#### Returns

Query class, class for querying DB
Type: *class*
