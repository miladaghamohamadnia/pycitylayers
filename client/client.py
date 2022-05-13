import yaml
import os
import requests
import json
from pprint import pprint
from shapely.geometry import Polygon, Point, box
from ..queries import query_gql_all_tables, query_gql_all_columns, query_gql_rows

#

class Client:
    def __init__(self, source="cerc"):
        self._source = source
        ### read config yaml 
        self._read_config() 
        ### get url matching the provided source
        self._url = self._get_url(source) 
        
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url
    
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

            
    @staticmethod
    def _geometry_validator(geom):
        return True
    
    
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
    
    
    def _read_config(self):
        with open(os.path.join(os.getcwd(), "pycitylayers/configs.yaml"), "r") as f:
            try:
                self._configs = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
            
            
    def _get_url(self, source):
        try:
            return self._configs["urls"][source]
        except:
            raise ValueError("invalid source provided!")
        return None
    
    def _execute_query(self, query_json):
        req = requests.post(url=self._url, json=query_json, headers={})
        res = Response()
        res.from_requests(req)
        return res
    

    
class Response:
    def __init__(self):
        pass
    
    def from_requests(self, res):
        self._res_text = res.text
        
    def to_json(self):
        json_obj = json.loads(self._res_text)
        self._res_json = json_obj
        return json_obj
    
    
    
    
class GeometryGQL:
    def __init__(self):
        pass
    
    def format_geom(self, coords, epsg=4326, geom_type='Polygon'):
        formatted_geom = {
                            "geometry": {
                                "type": geom_type,
                                "coordinates": coords,
                                "crs":{"type":"name","properties":{"name":f"EPSG:{epsg}"}}
                            }
                        }
        return formatted_geom
    
    
class PointGQL(GeometryGQL):
    def __init__(self):
        super().__init__()
        self.geom_type = "Point"
    
    def point(self, x, y):
        point = Point(x, y)
        point = [xy[0] for xy in point.coords.xy]
        return self.format_geom(point, geom_type=self.geom_type)
    
class PolygonGQL(GeometryGQL):
    def __init__(self):
        super().__init__()
        self.geom_type = "Polygon"
    
    def rect_from_two_corners(self, p1, p2):
        xmin = min(p1[0], p2[0])
        xmax = max(p1[0], p2[0])
        ymin = min(p1[1], p2[1])
        ymax = max(p1[1], p2[1])
        rect = box(xmin,ymin,xmax,ymax)
        rect_xy = [list(xy) for xy in list(zip(rect.exterior.coords.xy[0], rect.exterior.coords.xy[1]))]
        return self.format_geom([rect_xy], geom_type=self.geom_type)
    
    def poly_from_points(self, points):
        return self.format_geom([points], geom_type=self.geom_type)
    