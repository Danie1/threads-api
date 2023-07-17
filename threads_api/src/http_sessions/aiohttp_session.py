import aiohttp
import json

from threads_api.src.http_sessions.abstract_session import HTTPSession
from threads_api.src.anotherlogger import log_debug

from instagrapi import Client

class AioHTTPSession(HTTPSession):
    def __init__(self):
        self._session = aiohttp.ClientSession()
        self._instagrapi_client = Client()

    async def start(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

        if self._instagrapi_client is None:
            self._instagrapi_client = Client()

    async def close(self):
        await self._session.close()
        self._session = None
        self._instagrapi_client = None

    def auth(self, **kwargs):
        self._instagrapi_client.login(**kwargs)
        token = self._instagrapi_client.private.headers['Authorization'].split("Bearer IGT:2:")[1]
        return token
    
    async def post(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='POST', **kwargs)
        async with self._session.post(**kwargs) as response:
            try:
                text = await response.text()
                resp = json.loads(text)
                log_debug(title='PRIVATE RESPONSE', response=resp)

                if resp['status'] == 'fail':
                    raise Exception(f"Request Failed: [{resp['message']}]")
            except (aiohttp.ContentTypeError, json.JSONDecodeError):
                raise Exception('Failed to decode response as JSON')
            
            return resp

    async def get(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='GET', **kwargs)
        async with self._session.get(**kwargs) as response:
            try:
                text = await response.text()
                resp = json.loads(text)
                log_debug(title='PRIVATE RESPONSE', response=resp)

                if resp['status'] == 'fail':
                    raise Exception(f"Request Failed: [{resp['message']}]")
            except (aiohttp.ContentTypeError, json.JSONDecodeError):
                raise Exception('Failed to decode response as JSON')
            
            return resp


