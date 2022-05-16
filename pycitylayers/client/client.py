from __future__ import annotations
from ..query import QueryGQL, QueryCKAN
from ..utils import URLS
#


class Client:
    def __init__(self):
        pass
    
    @staticmethod
    def create(*args, **kwargs):
        if not 'source' in kwargs:
            raise ValueError("invalid source provided!")
        else:
            if kwargs['source']=="quebec":
                return QueryCKAN(*args, **kwargs)
            elif kwargs['source']=="cerc":
                return QueryGQL(*args, **kwargs)
            else:
                raise ValueError("invalid input provided!")
            
        

    
    
    