import ripio
import requests
from ripio.exceptions.auth import UnathorizedClient

class RipioClient(object):
    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.api_key = ripio.api_key if api_key is None else api_key
        
    def get(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        response = self.session.get(*request_args, **request_kwargs)
        return response
        
        
    def put(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        response =self.session.get(*request_args, **request_kwargs)
        return response
         
    
    def post(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        response = self.session.post(*request_args, **request_kwargs)
        return response
        
    def delete(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        response = self.session.delete(*request_args, **request_kwargs)
        return response
        
    def check_api_key(func):
        def checker(self, *args, **kwargs):
            if self.api_key is None:
                raise UnathorizedClient("No credenatials were passed")
            func(self, *args, **kwargs)
        return checker