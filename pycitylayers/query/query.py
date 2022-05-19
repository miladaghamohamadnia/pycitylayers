# -*- coding: utf-8 -*-
"""
Query classes for querying of DB
"""

from __future__ import annotations
import yaml
import os
import requests
from ..utils import query_gql_all_tables, query_gql_all_columns, query_gql_rows
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
    
        

class QueryGQL(Query):
    """
        GraphQL Querying class  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_all_tables(self):
        schema = self._fetch_schema()
        json_schema = schema.to_json()
        if self._source == 'cerc':
            items = json_schema['data']['__schema']['queryType']['fields']
            items = [resp['name'] for resp in items]
            return items
            

    def get_columns(self, table=""):
        if len(table)>0 and self._source == 'cerc':
            query_json = query_gql_all_columns(table)
            schema = self._execute_query(query_json)
            json_schema = schema.to_json()
            items = json_schema['data']['__type']
            if items: 
                items = [resp['name'] for resp in items['fields']]
            else:
                items = []
            return items
    
    def get_rows(self, **kwargs):
        if 'geometry' in kwargs:
            self._geometry_validator(kwargs['geometry'])
        query_json = query_gql_rows(**kwargs)
        packet = self._execute_query(query_json)       
        json_packet = packet.to_json()
        if 'data' in json_packet:
            data = json_packet['data']  
        else:
            data={}
        return data
        
        
    def _fetch_schema(self):
        query_json = query_gql_all_tables()
        res = self._execute_query(query_json)
        return res
    
            
    def _get_url(self, source):
        try:
            return URLS[source]
        except:
            raise ValueError("invalid source provided!")
        return None
    
    
    def _execute_query(self, query_json):
        req = requests.post(url=self._url, json=query_json, headers={})
        res = Response()
        res.from_requests(req)
        return res
    


class QueryCKAN(Query):
    """
        CKAN Querying class  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("##############")
        self._collection = None

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
        print(len(_schema))
        self._collection = _schema
    
    def _load_collection(self):
        pass
        """
            Method to retrieve/fetch the entire metadata object from ckan endpoint
            
            :return: List of datasets aka. the metadata collection
            :rtype: List of objects
        """
        # print( os.path.join(os.path.dirname(__file__), '..') )
        # with open(fpath, 'r') as f:
        #     _schema = json.load(f)
        # self._collection = _schema
        
    @property
    def collection(self):
        """
            Returns datasets collection of current data source. 
            This function will trigger metadata fetch if not done yet
            
            :return: The metadata collection
            :rtype: List of objects
        """
        if self._collection is None: self._fetch_collection()
        return self._collection
        
