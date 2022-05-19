import pandas as pd
import numpy as pd

class Collection:
    """
        class representing info and methods available for interacting
            with a collection of datasets
    """
    def __init__(self, source="cerc"):
        self._datasets = []
        self._source = source
    def from_dict(self, collection_dict):
        """
            imports a dictionary object representing the data collection metadata.
            
            :param collection_dict: dict, dictionary of data collection metadata
            :return: None
        """
        self._metadata = collection_dict
        self._datasets = []
        for dataset_dict in collection_dict:
            d = Dataset()
            d.from_dict(dataset_dict)
            self._datasets.append(d)
    def __len__(self):
        return len(self._datasets)
    def __getitem__(self, index):
        return self._datasets[index]
    @property
    def metadata(self):
        """
            returns the metadata dict loaded previously into the class.
            :return: dict, metadata dict of data collection loaded.
        """
        self.is_data_loaded()
        return self._metadata
    def search(self, by_tag=None, by_name=None, return_indices=False):
        """
            searches the collection of datasets to return 
                datasets that satisfy the specified criteria.
            
            :param by_name: string, search by name if a dataset name attribute contains the given string
                default: None, which doesn't use this search criterion
            :param by_tag: string, search by tag string if any of dataset tags contains the given string
                default: None, which doesn't use this search criterion
            :param return_indices: bool, flag for returning the indices of found datasets as well.
                default: False, which doesn't return indices of found datasets
            :return: list|tuple, list of Dataset instances matching the search condition OR a tuple 
                containing the return indices if return_indices flag is True.

        """
        self.is_data_loaded()
        datasets = C._datasets
        indices = list(range(len(C)))
        
        if not (by_name is None):
            indices = [ix for ix, ds in zip(indices, datasets) if by_name in ds._name ]
            datasets = [C._datasets[ix] for ix in indices]
        if not (by_tag is None):
            indices = [ix for ix, ds in zip(indices, datasets) if by_tag in ds._tags ]
            datasets = [C._datasets[ix] for ix in indices]            
        if return_indices:
            return (datasets, indices)
        else:
            return datasets
    def is_data_loaded(self):
        """
            checks if any data has been loaded to work with.
                throws a ValueError in the absence of a data 
                collection and stops the flow of the code.
                
            :raises: ValueError, when there is no data loaded.
        """
        try:
            self._datasets[0]
        except:
            raise ValueError("no dataset loaded to work with!")
    def __repr__(self):
        """repr method showing most important attributes of the class"""
        return f"{10*'-'} Data Collection {10*'-'}\nSource:\t\t{self._source} \nDatasets Count:\t{len(self)}"

        
    
class Dataset:
    """
        class representing info and methods available for interacting
            with a dataset. a dataset instance is a collection of data tables.
    """
    def __init__(self):
        self._tables = []
    def from_dict(self, dataset_dict):
        """
            imports a dictionary object representing the dataset metadata.
            
            :param dataset_dict: dict, dictionary of dataset metadata
            :return: None
        """
        attrs = ['id', 'metadata_created', 'num_tags'
                 'author', 'title', 'name', 'url', 'notes', 
                 'update_frequency', 'metadata_modified']
        for attr in attrs:
            if attr in dataset_dict:
                setattr(self, "_"+attr, dataset_dict[attr])
            else:
                setattr(self, "_"+attr, None)
                
        self._num_resources = len(dataset_dict['resources'])
        self._tags = [tag['name'] for tag in dataset_dict['tags']]
        
        self._tables = []
        for table_dict in dataset_dict['resources']:
            t = Table()
            t.from_dict(table_dict)
            self._tables.append(t)
    @property
    def tables(self):
        """
            returns the tables metadata dict loaded previously into the class.
            :return: dict, tables metadata dict of data collection loaded.
        """
        return self._tables
    def __repr__(self):
        """repr method showing most important attributes of the class"""
        return f"{10*'-'} Dataset {10*'-'}\nName:\t\t{self._title} \nTables Count:\t{self._num_resources} \nCreated:\t{self._metadata_created} \n"
    def __getitem__(self, index):
        return self._tables[index]


class Table:
    """
        class representing info and methods available for 
            interacting with a data table. a table 
            instance is a collection of data columns and rows.
    """
    def __init__(self):
        self._columns = []
        self._num_columns = 0
        self._table_meta = {}
    def from_dict(self, table_dict):
        """
            imports a dictionary object representing a table metadata.
            
            :param table_dict: dict, dictionary of table metadata
            :return: None
        """
        attrs = ['id', 'format','name', 'description', 'created', 
                 'last_modified', 'url', 'resource_type', 'position']
        for attr in attrs:
            if attr in table_dict:
                setattr(self, "_"+attr, table_dict[attr])
            else:
                setattr(self, "_"+attr, None)
    def __repr__(self):
        """repr method showing most important attributes of the class"""
        return f"{10*'-'} Table:{self._position} {10*'-'}\nName:\t\t{self._name} \nDescription:\t{self._description} \nFormat:\t\t{self._format} \n"
    def query_simple(self, nrows=1, offset=0, as_df=True):
        data = []
        step = 1000
        lm = min(nrows, step)
        of = offset
        flag = True
        while flag:
            if (of-offset+lm)>=nrows: 
                lm=nrows-(of-offset)
                flag = False
            url = f"{_url}/datastore_search?limit={lm}&offset={of}&resource_id={self._id}"
            of += lm
            res = requests.get(url).json()['result']['records']
            data += res
            offset += step
        if as_df: return pd.DataFrame.from_dict(data, orient='columns')
        return data
    
    def _fetch_table_meta(self):
        url = f"{_url}/datastore_search?limit=0&resource_id={self._id}"
        self._table_meta = requests.get(url).json()['result']
        self._columns = [c['id'] for c in self._table_meta['fields']]
        self._num_columns = int(self._table_meta['total'])
        return self._table_meta
    @property
    def columns(self):
        if self._num_columns==0: self._fetch_table_meta()
        return self._columns
        