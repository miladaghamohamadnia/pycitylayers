from gql_query_builder import GqlQuery
from pprint import pprint
from .constants import GEOM_OPT_MAPPING
#

def query_gql_all_tables():
    query = GqlQuery().fields(['name']).query('fields').operation('queryType').generate()
    query = GqlQuery().fields([query]).query('__schema').generate()
    query = GqlQuery().fields([query]).generate()
    return { 'query' :  query }

def query_gql_all_columns(table_name):
    query = GqlQuery().fields(['name']).query('fields').generate()
    query = GqlQuery().fields([query]).query('__type', input={'name': f'"{table_name}"'}).generate()
    query = GqlQuery().fields([query]).generate()
    json_query = { 'query' :  query }
    return json_query

def query_gql_rows(table="", columns=[], nrows=5, skiprows=0, geometry=None, geometry_operation='is_within_poly', **kwargs):
    if geometry is None:
        query = GqlQuery().fields(columns).query(name=table, input={'limit': nrows, 'offset': skiprows}).generate()
        query = GqlQuery().operation(name='getrows', queries=[query]).generate()
        json_query = { 'query' :  query }
    else:
        geometry_operation = GEOM_OPT_MAPPING[geometry_operation]
        if geometry_operation=='_st_within':
            where_clause = {'geom': {geometry_operation: '$geometry'}}
        elif geometry_operation=='_st_d_within' and 'geom_distance' in kwargs:
            d = kwargs['geom_distance']
            where_clause  = {'geom': {geometry_operation: {'distance': d, 'from':'$geometry' }}}
        else: 
            raise ValueError("invalid geometry_operation provided!")
        query = GqlQuery().fields(columns).query(name=table, input={'limit': nrows, 'offset': skiprows, 'where': where_clause}).generate()
        query = GqlQuery().operation(name='getrows', queries=[query], input={'$geometry': 'geometry!'}).generate()
        query = query.replace("'","")
        json_query = { 'query' :  query, 'variables':  geometry}
    return json_query


