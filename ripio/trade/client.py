import ripio
from ripio.core import RipioClient
from ripio.exceptions.request import InvalidParamaters


class Client(RipioClient):
    def __init__(self, api_key=None):
        self.base_url = ripio.RIPIO_TRADE_BASE_URL
        super().__init__(api_key)

    def authenticate_session(self):
        self.session.headers["Authorization"] = self.api_key

    @RipioClient.check_api_key
    def get_orders(
        self,
        pair,
        status=None,
        side=None,
        type=None,
        ids=None,
        start_date=None,
        end_date=None,
        page_size=None,
        current_page=None,
    ):
        function_params = locals()
        params = {
            key: function_params[key]
            for key in function_params
            if key != "self" and function_params[key] is not None
        }

        response = self.get(
            f"{self.base_url}orders", params=params, success_status_code=200
        )
        return response

    @RipioClient.check_api_key
    def create_orders(
        self,
        pair,
        side,
        type,
        amount=None,
        price=None,
        value=None,
    ):
        if type == "limit" and (amount is None or price is None):
            if amount is None:
                raise InvalidParamaters("The amount can not be null")
            else:
                raise InvalidParamaters("The price can not be null")
        request_dict = {
            "pair": pair,
            "side": side,
            "amount": amount,
            "price": price,
            "value": value,
        }
        request_body = self.remove_null_from_request_body(request_dict)
        response = self.post(
            f"{self.base_url}orders",
            json=request_body,
            success_status_code=200,
        )
        return response

    def get_tickers(self):
        response = self.get(
            f"{self.base_url}public/tickers", success_status_code=200
        )
        return response
