# -*- coding: utf-8 -*-
"""
Query classes for querying of DB
"""

from __future__ import annotations
import yaml
import os
import requests
from ..utils import CKANCollection, GQLCollection
from ..utils import query_gql_all_tables
# from ..utils import query_gql_all_columns, query_gql_rows
from ..utils import get_project_root
from ..utils import Response
from ..utils import URLS

__author__ = "Milad Aghamohamadnia"
__copyright__ = "Copyright 2022, CERC Concordia University - Montreal, CANADA"
__credits__ = ["Ursula Eicker", "Milad Aghamohamadnia"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Milad Aghamohamadnia"
__email__ = "milad.aghamohamadnia"
__status__ = "Development"


class Query:
    """
        Base Query class  
    """
    def __init__(self, *args, **kwargs):
        self._source = kwargs['source']
        ### get url matching the provided source
        self._url = self._get_url(self._source) 

    @staticmethod
    def _geometry_validator(geom):
        """
            method to check if an input geometry is valid  
            
            :param geom: geometry in the form of geojson string
            :type geom: string
            :return: flag of validity
            :rtype: bool
        """
        return True
    
    @property
    def url(self):
        """
            property method to get current url of DB api 
            
            :return: url string
            :rtype: string
        """
        return self._url
    
    @url.setter
    def url(self, url):
        """
            method to set current url of DB api  
            
            :param url: url of DB api  
            :type url: string
        """
        self._url = url
       
    @staticmethod
    def _get_url(source):
        """
            method to return DB url from dictionary of urls
            
            :param source: name of DB source
            :type source: string
            :return: url of DB api
            :rtype: string
        """
        try:
            return URLS[source]
        except:
            raise ValueError("invalid source provided!")
        return None
    
    @property
    def collection(self) -> list:
        return self._collection
    
    def query(self):
        pass
        
    
    
        

class QueryGQL(Query):
    """
        GraphQL Querying class  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._schema = self._fetch_collection()
        self._collection = GQLCollection(source=self._source, schema=self._schema, rooturl=self._url)
        
    def _fetch_collection(self):
        query_json = query_gql_all_tables()
        _schema = self._execute_query(query_json)
        return _schema
        
    def _execute_query(self, query_json):
        req = requests.post(url=self._url, json=query_json, headers={})
        res = Response()
        res.from_requests(req)
        return res
    
    def query(self, table, columns=[], conditions=[], condition_operator=None, nrows=1, skiprows=0, geometry=None, geometry_operation='is_within_poly', as_df=True, *args, **kwargs):
        datasets, indices = self._collection.search(by_name=table, return_indices=True)
        if len(indices)<1: 
            raise ValueError('No data was found')
        if len(indices)>1: 
            print('Warning: more than one data was found. returning the first dataset')

        dataset = datasets[0]
                
        tables = [table for table in  dataset.tables if table._format=='CSV']
        
        if len(tables)>0:
            table = tables[0]
            data = table.query_sql(columns=columns, 
                                            conditions=conditions, 
                                            condition_operator=condition_operator, 
                                            nrows=nrows, 
                                            offset=skiprows, 
                                            as_df=as_df)
        else:
            raise ValueError('Non of data found was queryable!')
        return data
    


class QueryCKAN(Query):
    """
        CKAN Querying class  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._schema = self._fetch_collection()
        self._collection = CKANCollection(source=self._source, schema=self._schema, rooturl=self._url)

    def _fetch_collection(self):
        """
            Method to retrieve/fetch the entire metadata object from ckan endpoint
            
            :return: List of datasets aka. the metadata collection
            :rtype: List of objects
        """
        _schema = []
        offset = 0
        step = 500
        while True:
            url = f"{self._url}/current_package_list_with_resources?limit={step}&offset={offset}"
            res = requests.get(url).json()['result']
            if len(res)==0: break
            _schema += res
            offset += step
        return _schema
    
    
    def query(self, table, columns=[], conditions=[], condition_operator=None, nrows=1, skiprows=0, as_df=True, *args, **kwargs):
        datasets, indices = self._collection.search(by_name=table, return_indices=True)
        if len(indices)<1: 
            raise ValueError('No data was found')
        if len(indices)>1: 
            print('Warning: more than one data was found. returning the first dataset')

        dataset = datasets[0]
                
        tables = [table for table in  dataset.tables if table._format=='CSV']
        
        if len(tables)>0:
            table = tables[0]
            data = table.query_sql(columns=columns, 
                                            conditions=conditions, 
                                            condition_operator=condition_operator, 
                                            nrows=nrows, 
                                            offset=skiprows, 
                                            as_df=as_df)
        else:
            raise ValueError('Non of data found was queryable!')
        return data
        




