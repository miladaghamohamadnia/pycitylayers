from __future__ import annotations
import yaml
import os
import requests
# import json
# from pprint import pprint
from ..utils import query_gql_all_tables, query_gql_all_columns, query_gql_rows
from ..utils import get_project_root
from ..utils import Response
from ..utils import URLS



class Query:
    def __init__(self, *args, **kwargs):
        
        self._source = kwargs['source']
        ### get url matching the provided source
        self._url = self._get_url(self._source) 

    @staticmethod
    def _geometry_validator(geom):
        return True
    
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url
       
    @staticmethod
    def _get_url(source):
        try:
            return URLS[source]
        except:
            raise ValueError("invalid source provided!")
        return None
    
        
class QueryCKAN(Query):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
class QueryGQL(Query):
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
    
