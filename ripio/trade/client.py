from ripio.core import RipioClient

class Client(RipioClient):
    def __init__(self, api_key = None):
        self.require_authorization = True
        super().__init__(api_key)
