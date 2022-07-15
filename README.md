# pycitylayers


This is a Python API to interact with Concordia CERC's open data and other available external open portals.

It uses GraphQL and PostGIS for geometrical queries. Meanwhile can handle CKAN backed data storages.

## Documentation

- Here is the [Documentation](https://miladaghamohamadnia.github.io/pycitylayers/) for this project

## Install

install anaconda or miniconda if not already done

create a virtual env
```shell
conda create -n pycl python=3.9
conda activate pycl
```

clone and install the package

```shell
git clone https://github.com/miladaghamohamadnia/pycitylayers.git
cd pycitylayers
pip install .
```

if GDAL error happens:
install GDAL via conda prior to pip installing
```shell
conda install GDAL
```


## Structure
Database --> 
Collection -->
Dataset -->
Tables



## Usage

- get all data datasets available

```python
from pycitylayers.client import Client
from pycitylayers.utils import PointGQL, PolygonGQL

client = Client().create(source='cerc')
coll = client.collection

datasets = coll.datasets

pprint(datasets)

```


- get 5 rows from a table

```python
from pycitylayers.client import Client
from pycitylayers.utils import PointGQL, PolygonGQL

client = Client().create(source='cerc')
coll = client.collection
dataset = coll[2]
table = dataset[0]

query_options = {
    'columns': ['code', 'name', 'year'], 
    'nrows': 5, 
    'skiprows': 3,
}

data = table.query_simple( **query_options )
print(data)

```
