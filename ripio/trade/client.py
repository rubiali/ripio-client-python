from ripio.core import RipioClient
import ripio

class Client(RipioClient):
    def __init__(self, api_key = None):
        self.require_authorization = True
        self.base_url = ripio.RIPIO_TRADE_BASE_URL
        super().__init__(api_key)
        
        
    @RipioClient.check_api_key
    def get_orders(self,*args, **kwargs):
        response = self.get(f"{self.base_url}orders")
