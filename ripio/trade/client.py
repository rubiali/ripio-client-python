import ripio
import datetime as dt
from ripio.core import RipioClient
from ripio.exceptions.request import InvalidParamaters


class Client(RipioClient):
    def __init__(self, api_key=None, api_secret=None):
        self.base_url = ripio.RIPIO_TRADE_BASE_URL
        super().__init__(api_key, api_secret)

    def authenticate_session(self):
        self.session.headers["Authorization"] = self.api_key

    # Orders Management
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
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}orders", params=params, success_status_code=200
        )
        return response

    @RipioClient.check_api_key
    def create_order(
        self,
        pair,
        side,
        type,
        amount=None,
        price=None,
        value=None,
        external_id=None,
    ):
        if type == "limit" and (amount is None or price is None):
            if amount is None:
                raise InvalidParamaters("The amount can not be null")
            else:
                raise InvalidParamaters("The price can not be null")
        request_dict = {
            "type": type,
            "pair": pair,
            "side": side,
            "amount": amount,
            "price": price,
            "value": value,
            "external_id": external_id,
        }
        request_body = self.remove_null_from_request_body(request_dict)
        response = self.post(
            f"{self.base_url}orders",
            json=request_body,
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def cancel_order(self, id):
        request_body = {"id": id}
        response = self.delete(
            f"{self.base_url}orders",
            json=request_body,
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def get_open_orders(self, pair, side, page_size=None, current_page=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}orders/open",
            params=params,
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def get_order_by_id(self, id):
        response = self.get(
            f"{self.base_url}orders/{id}",
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def get_order_by_external_id(self, external_id):
        response = self.get(
            f"{self.base_url}orders/by-external-id/{external_id}",
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def cancel_order_by_external_id(self, external_id):
        request_body = {"external_id": external_id}
        response = self.delete(
            f"{self.base_url}orders/by-external-id",
            json=request_body,
            success_status_code=200,
        )
        return response

    @RipioClient.check_api_key
    def cancel_all_orders(self):
        response = self.delete(
            f"{self.base_url}orders/all",
            success_status_code=200,
        )
        return response

    # Public Endpoints
    def get_tickers(self):
        response = self.get(
            f"{self.base_url}public/tickers", success_status_code=200
        )
        return response

    def get_ticker_by_pair(self, pair):
        response = self.get(
            f"{self.base_url}public/tickers/{pair}", success_status_code=200
        )
        return response

    def get_orderbook_level_3(self, pair, limit=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}public/orders/level-3", 
            params=params,
            success_status_code=200
        )
        return response

    def get_orderbook_level_2(self, pair, limit=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}public/orders/level-2", 
            params=params,
            success_status_code=200
        )
        return response

    def get_trades(self, pair, start_time=None, end_time=None, page_size=None, current_page=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}public/trades", 
            params=params,
            success_status_code=200
        )
        return response

    def get_currencies(self, currency_code=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}public/currencies", 
            params=params,
            success_status_code=200
        )
        return response

    def get_pairs(self, pair=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}public/pairs", 
            params=params,
            success_status_code=200
        )
        return response

    def get_server_time(self):
        response = self.get(
            f"{self.base_url}public/server-time",
            success_status_code=200
        )
        return response

    # Book endpoints
    @RipioClient.check_api_key
    def get_book_summary(self, pair):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}book/summaries",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_book_estimate_price(self, pair, amount, side):
        function_params = locals()
        params = self.get_params_from_locals(function_params, ['pair'])
        response = self.get(
            f"{self.base_url}book/estimate-price/{pair }",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_book_orderbook_level_3(self, pair, limit=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}book/orders/level-3",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_book_orderbook_level_2(self, pair, limit=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}book/orders/level-2",
            params=params,
            success_status_code=200   
        )
        return response

    # User Endpoints
    @RipioClient.check_api_key
    def get_user_balances(self):
        response = self.get(
            f"{self.base_url}user/balances",
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_user_balance_on_date(self, date):
        if not isinstance(date, dt.date):
            raise InvalidParamaters("'date' must be a datetime.date instance")
        formatted_date = date.isoformat()
        response = self.get(
            f"{self.base_url}user/balances/{formatted_date}",
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_user_fee_and_limits(self):
        response = self.get(
            f"{self.base_url}user/fees-and-limits",
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_user_statement(self, start_time=None, end_time=None, page_size=None, current_page=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}user/statement",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_user_statement_by_currency(self, currency_code, start_time=None, end_time=None, page_size=None, current_page=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params, ['currency_code'])
        response = self.get(
            f"{self.base_url}user/statement/{currency_code}",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def get_user_trades(self, start_time=None, end_time=None, page_size=None, current_page=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}user/trades",
            params=params,
            success_status_code=200   
        )
        return response

    # Deposit Endpoints
    @RipioClient.check_api_key
    def get_deposits(self, currency_code, status, start_time=None, end_time=None, page_size=None, current_page=None, network=None):
        function_params = locals()
        params = self.get_params_from_locals(function_params)
        response = self.get(
            f"{self.base_url}deposits",
            params=params,
            success_status_code=200   
        )
        return response

    @RipioClient.check_api_key
    def list_cryptocurrency_withdrawals(
        self, currency_code=None, status=None, start_date=None, end_date=None, 
        page_size=200, current_page=1, network=None
    ):
        params = {
            "currency_code": currency_code,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
            "page_size": page_size,
            "current_page": current_page,
            "network": network
        }
        response = self.get(
            f"{self.base_url}withdrawals", 
            params=params, 
            success_status_code=200
        )
        return response

    @RipioClient.check_api_key
    def create_cryptocurrency_withdrawal(
        self, amount, destination, currency_code, external_id=None, tag=None, 
        network=None, memo=None
    ):
        request_body = {
            "external_id": external_id,
            "tag": tag,
            "network": network,
            "memo": memo,
            "amount": amount,
            "destination": destination,
            "currency_code": currency_code
        }
        response = self.post(
            f"{self.base_url}withdrawals", 
            json=request_body, 
            success_status_code=200
        )
        return response

    @RipioClient.check_api_key
    def estimate_withdrawal_fee(self, currency_code, network=None, amount=None):
        params = {"network": network, "amount": amount}
        response = self.get(
            f"{self.base_url}withdrawals/estimate-fee/{currency_code}", 
            params=params, 
            success_status_code=200
        )
        return response

    @RipioClient.check_api_key
    def get_cryptocurrency_withdrawal(self, id=None, external_id=None):
        params = {"id": id, "external_id": external_id}
        response = self.get(
            f"{self.base_url}withdrawals/withdrawal", 
            params=params, 
            success_status_code=200
        )
        return response
