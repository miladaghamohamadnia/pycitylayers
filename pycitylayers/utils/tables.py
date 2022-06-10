import requests
import json
from pprint import pprint
import numpy as np
import os
import pandas as pd
from jinjasql import JinjaSql
import wget
from . import query_gql_all_columns, query_gql_rows, query_gql_num_rows
from . import Response
from ckanapi import RemoteCKAN


class Table:
    def __init__(self, url=""):
        self._columns = []
        self._num_columns = 0
        self._num_rows = None
        self._table_meta = {}
        self.rooturl = url
    
    def load_from(self, table_dict):
        """ imports a dictionary object representing a table metadata.
            
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
      
      

class GQLTable(Table):
    def __init__(self, url=""):
        super().__init__(url=url)
    
    def _fetch_columns_info(self):
        query_json = query_gql_all_columns(self._name)
        schema = self._execute_query(query_json)
        self._table_meta = schema.to_json()
        items = self._table_meta['data']['__type']
        if items:
            items = [resp['name'] for resp in items['fields']]
        else:
            items = []
        self._columns = items
        self._num_columns = len(self._columns)
        return self._table_meta
    
    def _fetch_rows_info(self):
        query_json = query_gql_num_rows(self._name)
        schema = self._execute_query(query_json)
        schema = schema.to_json()
        # {'data': {'bixi_trips_aggregate': {'aggregate': {'count': 29460723}}}}
        count = list(schema['data'].values())[0]['aggregate']['count']
        self._num_rows = count
        return self._num_rows
    
    def __len__(self) -> int:
        return self._num_rows
    
    @property
    def num_rows(self):
        if not self._num_rows: self._fetch_rows_info()
        return self._num_rows
    
    @property
    def size(self):
        if not self._num_columns : self._fetch_columns_info()
        if not self._num_rows : self._fetch_rows_info()
        return (self._num_rows, self._num_columns)
    
    @property
    def columns(self) -> list:
        """_summary_

        Returns
        -------
        list
            _description_
        """
        if not self._num_columns: self._fetch_columns_info()
        return self._columns
    
    def _execute_query(self, query_json):
        req = requests.post(url=self.rooturl, json=query_json, headers={})
        res = Response()
        res.from_requests(req)
        return res

    def query_simple(self, columns=[], nrows:int = 3, skiprows:int = 0, as_df:bool = True, *args, **kwargs):
        # if 'geometry' in kwargs:
        #     self._geometry_validator(kwargs['geometry'])
        if len(columns)==0:
            columns = self.columns
        query_json = query_gql_rows(self._name, columns, nrows, skiprows, *args, **kwargs)
        packet = self._execute_query(query_json)
        json_packet = packet.to_json()
        if 'data' in json_packet:
            data = json_packet['data']  
        else:
            data={}
        if as_df and self._name in data: 
            return pd.DataFrame.from_dict(data[self._name], orient='columns')
        return data
    
    

class CKANTable(Table):
    """
        class representing info and methods available for 
            interacting with a data table. a table 
            instance is a collection of data columns and rows.
    """
    def __init__(self, url=""):
        super().__init__(url=url)
        self.remote_handle = RemoteCKAN(url.split("/r")[0], user_agent="")
    
    def query_simple(self, nrows:int = 1, skiprows:int = 0, columns=[], as_df:bool = True) -> pd.DataFrame:
        self._check_queryable()
        
        query_params = {
            # 'filters': {'EXVILLE':'Buckingham'},
            'limit': nrows, 
            'offset': skiprows
        }
        
        if len(columns)>0: 
            query_params['fields'] = columns
        data = []
        step = 1000
        if nrows==0: 
            if self._num_rows==0: self._fetch_table_meta()
            nrows = self._num_rows
        n = int(np.ceil(nrows/step))
        r = nrows%step
        indices = [skiprows+el*step for el in range(n)] + [nrows+skiprows]
        for ix1, ix2 in zip(indices[:-1], indices[1:]):
            query_params['limit'] = ix2 - ix1
            query_params['offset'] = ix1
            res = self.remote_handle.action.datastore_search(resource_id = self._id, **query_params)
            try:
                res = res['records']
            except:
                raise ValueError(f"No data was found. below is the content found: \n{res}")
                continue
            data += res
        if as_df: return pd.DataFrame.from_dict(data, orient='columns')
        return data
    
    def query_sql(self, sql_str, as_df=True):
        ## TODO: expose conditions parameter to api upon debugging issue
        self._check_queryable()
        data = self.remote_handle.action.datastore_search_sql(sql=sql_str)
        # data = packet.json()
        try:
            # data = data['result']['records']
            data = data['records']
        except:
            raise ValueError(f"No data was found. below is the content found: \n{data}")
        if as_df: return pd.DataFrame.from_dict(data, orient='columns')
        return data
    
    def _fetch_table_meta(self):
        self._check_queryable()
        url = f"{self.rooturl}/datastore_search?limit=0&resource_id={self._id}"
        self._table_meta = requests.get(url).json()['result']
        self._columns = [c['id'] for c in self._table_meta['fields']]
        self._num_columns = len(self._columns)
        self._num_rows = int(self._table_meta['total'])
        return self._table_meta
    
    @property
    def columns(self) -> list:
        """_summary_

        Returns
        -------
        list
            _description_
        """
        if self._num_columns==0: self._fetch_table_meta()
        return self._columns
    
    @property
    def num_rows(self):
        if self._num_columns==0: self._fetch_table_meta()
        return self._num_rows
    
    @property
    def size(self):
        if (not self._num_rows) or (not self._num_columns) : self._fetch_table_meta()
        return (self._num_rows, self._num_columns)
                
    @property
    def is_queryable(self):
        return self._format=="CSV"
    
    def _check_queryable(self):
        if self.is_queryable:
            pass
        else:
            raise ValueError(f"This table is {self._format} format and can't be queried. \n Only tables with CSV format can be queried")
    
    def to_file(self, output_dir:str = None):
        """ downloads the table when it cant be queried

        Args:
            output_dir (str, optional): dir to write file to . Defaults to None.
        """
        if output_dir is None:
            output_dir = "."
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = wget.download(self._url, out=output_dir)
        print(f"file ## {filename} ## was saved to file")
    
    