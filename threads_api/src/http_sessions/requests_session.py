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
        response = self._session.post(**kwargs)
        return response.text

    async def get(self, **kwargs):
        response = self._session.get(**kwargs)
        return response.text
    
    async def download(self, **kwargs):
        response = self._session.get(**kwargs, stream=True)
        response.raw.decode_content = True
        return response.content