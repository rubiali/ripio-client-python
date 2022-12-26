import ripio
import requests
from ripio.exceptions.auth import UnathorizedClient

class RipioClient(object):
    
    require_authorization = False
    
    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.api_key = ripio.api_key if api_key is None else api_key
        self.check_api_key()
        
    def get(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        self.session.get(*request_args, **request_kwargs)
        
    def put(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        self.session.get(*request_args, **request_kwargs)
    
    def post(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        self.session.post(*request_args, **request_kwargs)
        
    def delete(self, *args, **kwargs):
        request_args = args
        request_kwargs = kwargs
        self.session.delete(*request_args, **request_kwargs)
        
    def check_api_key(self):
        if self.api_key is None and self.require_authorization:
            raise UnathorizedClient("No credenatials were passed")