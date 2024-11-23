from abc import ABC, abstractmethod
from json import JSONDecodeError
import hmac
import hashlib
import base64
import time
import json
import requests
from urllib.parse import urlparse

import ripio
from ripio.exceptions.auth import UnathorizedClient
from ripio.exceptions.response import NotSuccessfulResponse


class RipioClient(ABC):
    auth_mandatory = False

    def __init__(self, api_key=None, api_secret=None):
        self.session = requests.Session()
        self.api_key = ripio.api_key if api_key is None else api_key
        self.api_secret = api_secret

    def serialize_body(self, body):
        if body is None:
            return ''
        else:
            def convert_numbers(obj):
                if isinstance(obj, dict):
                    return {k: convert_numbers(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numbers(v) for v in obj]
                elif isinstance(obj, (int, float)):
                    return str(obj)
                else:
                    return obj

            converted_body = convert_numbers(body)
            body_str = json.dumps(converted_body, separators=(',', ':'))
            return body_str

    def _generate_headers(self, method, url, body):
        timestamp = str(int(time.time() * 1000))
        method = method.upper()
        parsed_url = urlparse(url)
        path = parsed_url.path 

        # Serializar o corpo
        body_str = self.serialize_body(body)

        message = timestamp + method + path + body_str
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')

        headers = {
            'Authorization': self.api_key,
            'Timestamp': timestamp,
            'Signature': signature_base64
        }
        return headers

    """
    Client Manager Specific Methods
    """
    def get_params_from_locals(self, local_vars, exclude_vars=[]):
        return {
            key: local_vars[key]
            for key in local_vars
            if key != "self" and local_vars[key] is not None and key not in exclude_vars
        }

    def process_arguments(self, **kwargs):
        client_kwargs = {"success_status_code": kwargs["success_status_code"]}
        del kwargs["success_status_code"]
        request_kwargs = kwargs
        return request_kwargs, client_kwargs

    def process_response(self, response, client_kwargs):
        response_body = self.get_response_body(response)
        if "success_status_code" in client_kwargs:
            if response.status_code == client_kwargs["success_status_code"]:
                return response_body
            else:
                message = f"{response.status_code} : {response_body}"
                raise NotSuccessfulResponse(message)
        else:
            return response_body

    def get_response_body(self, response):
        try:
            json_body = response.json()
            if "data" in json_body:
                return json_body["data"]
            else:
                return json_body
        except JSONDecodeError:
            return response.text

    def remove_null_from_request_body(self, request_dict):
        return {
            key: value
            for key, value in request_dict.items()
            if value is not None
        }

    def check_api_key(func):
        def checker(self, *args, **kwargs):
            if self.api_key is None:
                raise UnathorizedClient("No credentials were passed")
            self.authenticate_session()
            return func(self, *args, **kwargs)

        return checker

    def check_api_auth(self):
        if self.api_key is None and self.auth_mandatory:
            message = "Auth credentials are mandatory for this client"
            raise UnathorizedClient(message)
        elif self.auth_mandatory:
            self.authenticate_session()

    # Destructor method to free up resources
    def __del__(self):
        self.session.close()

    # Abstract method used to enable children to implement their own Authentication
    # Over the session
    @abstractmethod
    def authenticate_session(self):
        pass

    """
    HTTP supported methods handlers
    """

    def get(self, url, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)

        method = 'GET'
        full_url = url
        body = None  # GET requests não têm corpo

        if self.api_key and self.api_secret:
            headers = self._generate_headers(method, full_url, body)
            if 'headers' in request_kwargs:
                request_kwargs['headers'].update(headers)
            else:
                request_kwargs['headers'] = headers

        response = self.session.get(full_url, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def post(self, url, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)

        method = 'POST'
        full_url = url

        body = None
        if 'json' in request_kwargs:
            body = request_kwargs.pop('json')
        elif 'data' in request_kwargs:
            body = request_kwargs.pop('data')

        body_str = self.serialize_body(body)

        if self.api_key and self.api_secret:
            headers = self._generate_headers(method, full_url, body)

            if 'headers' in request_kwargs:
                request_kwargs['headers'].update(headers)
            else:
                request_kwargs['headers'] = headers

        if 'headers' not in request_kwargs:
            request_kwargs['headers'] = {}
        if 'Content-Type' not in request_kwargs['headers']:
            request_kwargs['headers']['Content-Type'] = 'application/json'

        request_kwargs['data'] = body_str

        response = self.session.post(full_url, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def put(self, url, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)

        method = 'PUT'
        full_url = url
        body = None
        if 'json' in request_kwargs:
            body = request_kwargs.pop('json')
        elif 'data' in request_kwargs:
            body = request_kwargs.pop('data')

        body_str = self.serialize_body(body)

        if self.api_key and self.api_secret:
            headers = self._generate_headers(method, full_url, body)
            if 'headers' in request_kwargs:
                request_kwargs['headers'].update(headers)
            else:
                request_kwargs['headers'] = headers

        if 'headers' not in request_kwargs:
            request_kwargs['headers'] = {}
        if 'Content-Type' not in request_kwargs['headers']:
            request_kwargs['headers']['Content-Type'] = 'application/json'

        request_kwargs['data'] = body_str

        response = self.session.put(full_url, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def delete(self, url, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)

        method = 'DELETE'
        full_url = url
        body = None
        if 'json' in request_kwargs:
            body = request_kwargs.pop('json')
        elif 'data' in request_kwargs:
            body = request_kwargs.pop('data')

        body_str = self.serialize_body(body)

        if self.api_key and self.api_secret:
            headers = self._generate_headers(method, full_url, body)
            if 'headers' in request_kwargs:
                request_kwargs['headers'].update(headers)
            else:
                request_kwargs['headers'] = headers

        if 'headers' not in request_kwargs:
            request_kwargs['headers'] = {}
        if 'Content-Type' not in request_kwargs['headers']:
            request_kwargs['headers']['Content-Type'] = 'application/json'

        request_kwargs['data'] = body_str

        response = self.session.delete(full_url, **request_kwargs)
        return self.process_response(response, client_kwargs)
