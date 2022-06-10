# -*- coding: utf-8 -*-
"""
Client class facilitating querying of DB
"""


from __future__ import annotations
from ..query import QueryGQL, QueryCKAN
from ..utils import URLS
#

__author__ = "Milad Aghamohamadnia"
__copyright__ = "Copyright 2022, CERC Concordia University - Montreal, CANADA"
__credits__ = ["Milad Aghamohamadnia", "Ursula Eicker"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Milad Aghamohamadnia"
__email__ = "milad.aghamohamadnia@concordia.ca"
__status__ = "Development"


class Client:
    def __init__(self):
        pass
    
    @staticmethod
    def create(*args, **kwargs):
        """
        Factory method instantiating appropriate query class  
        all valuse passed to this function is passed down to corresponding class initialization
        
        :param source: source DB name based on their categories
        :type source: string
        :return: Query class, class for querying DB
        :rtype: class
        """
        if not 'source' in kwargs:
            raise ValueError("invalid source provided!")
        else:
            if kwargs['source']=="quebec":
                return QueryCKAN(*args, **kwargs)
            elif kwargs['source']=="cerc":
                return QueryGQL(*args, **kwargs)
            else:
                raise ValueError("invalid input provided!")
            
        

    
    
    