# pycitylayers


This is a Python API to interact with Concordia CERC's open data and other available open portals.

It uses GraphQL and PostGIS for geometrical queries.

## Documentation

- Here is the <a href="https://miladaghamohamadnia.github.io/pycitylayers/" target="_blank">documentation</a> for this project

## Install

### linux

install virtualenv if not already done
```shell
sudo pip install --upgrade virtualenv
```
create a virtual env

```shell
virtualenv -p python3 pycitylayers
```
clone and install the package

```shell
git clone https://github.com/miladaghamohamadnia/pycitylayers.git
cd pycitylayers
pip install .
```

### Windows

Install pip
Usually Python3 comes with pip preinstalled. If you get an error "pip command not found", use the following command to install pip:

Launch a command prompt if it isn't already open. To do so, open the Windows search bar, type cmd and click on the icon. Then, run the following command to download the get-pip.py file:

```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

To install PIP type in the following:

```shell
python get-pip.py
```

Now pip should work system wide.

install virtualenv
```shell
pip install --upgrade virtualenv
```
create a virtual env

```shell
virtualenv -p python3 pycitylayers
```

clone and install the package

```shell
git clone https://github.com/miladaghamohamadnia/pycitylayers.git
cd pycitylayers
pip install .
```


## Usage

- get all data tables available

```python
from pycitylayers.client import Client
from pycitylayers.utils import PointGQL, PolygonGQL
from pprint import pprint

client = Client().create(source='cerc')

tables = client.get_all_tables()

pprint(tables)

```


- get 5 rows from a table

```python
from pycitylayers.client import Client
from pycitylayers.utils import PointGQL, PolygonGQL
from pprint import pprint

client = Client().create(source='cerc')

query_options = {
    'table': 'agents', 
    'columns': ['id', 'vlon', 'vlat'], 
    'nrows': 5, 
    'skiprows': 3,
}

data = client.get_rows( **query_options )
pprint(data)

```


