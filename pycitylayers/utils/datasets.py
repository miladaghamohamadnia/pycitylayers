import requests
import json
from pprint import pprint
import numpy as np
import os
import pandas as pd
from jinjasql import JinjaSql
import wget
from .tables import CKANTable, GQLTable


class Dataset:
    def __init__(self, url=""):
        self._tables = []
        self.rooturl = url
        
    def __len__(self):
        return len(self._datasets)
    
    @property
    def tables(self):
        """
            returns the tables metadata dict loaded previously into the class.
            :return: dict, tables metadata dict of data collection loaded.
        """
        return self._tables

    def __getitem__(self, index):
        return self._tables[index]



class GQLDataset(Dataset):
    def __init__(self, url=""):
        super().__init__(url=url)
    
    def load_from(self, dataset_dict):
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
        self._tables = []
        for table_dict in dataset_dict['resources']:
             d = GQLTable(url=self.rooturl)
             d.load_from(table_dict)
             self._tables.append(d)
            
    def __repr__(self):
        """repr method showing most important attributes of the class"""
        return f"{10*'-'} Dataset {10*'-'}\nName:\t\t{self._name} \nTables Count:\t{self._num_resources} \n"
    




class CKANDataset(Dataset):
    """
        class representing info and methods available for interacting
            with a dataset. a dataset instance is a collection of data tables.
    """
    def __init__(self, url=""):
        super().__init__(url=url)
    
    def load_from(self, dataset_dict):
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
            t = CKANTable(url=self.rooturl)
            t.load_from(table_dict)
            self._tables.append(t)
            

    def __repr__(self):
        """repr method showing most important attributes of the class"""
        date = self._metadata_created.split("T")[0]
        return f"{10*'-'} Dataset {10*'-'}\nName:\t\t{self._title} \nTables Count:\t{self._num_resources} \nCreated:\t{date} \n"
    

