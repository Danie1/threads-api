import requests
import json

from threads_api.src.http_sessions.abstract_session import HTTPSession
from threads_api.src.anotherlogger import log_debug

from instagrapi import Client

class RequestsSession(HTTPSession):
    def __init__(self):
        self._session = requests.Session()
        self._instagrapi_client = Client()

    async def start(self):
        if self._session is None:
            self._session = requests.Session()

    async def close(self):
        self._session.close()
        self._session = None

    def auth(self, **kwargs):
        self._instagrapi_client.login(**kwargs)
        token = self._instagrapi_client.private.headers['Authorization'].split("Bearer IGT:2:")[1]
        return token

    async def post(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='POST', requests_session_params=vars(self._session), **kwargs)
        response = self._session.post(**kwargs)
        try:
            resp = response.json()
            log_debug(title='PRIVATE RESPONSE', response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp

    async def get(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='GET', **kwargs)
        response = self._session.get(**kwargs)
        try:
            resp = response.json()
            log_debug(title='PRIVATE RESPONSE', response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp