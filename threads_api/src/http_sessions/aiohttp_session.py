import aiohttp
import json

from threads_api.src.http_sessions.abstract_session import HTTPSession
from threads_api.src.threads_api import log

class AioHTTPSession(HTTPSession):
    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def start(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()
        self._session = None

    def auth(self, auth_callback_func, **kwargs):
        return auth_callback_func(**kwargs)
    
    async def post(self, **kwargs):
        log(title='PRIVATE REQUEST', type='POST', **kwargs)
        async with self._session.post(**kwargs) as response:
            try:
                text = await response.text()
                resp = json.loads(text)
                log(title='PRIVATE RESPONSE', response=resp)

                if resp['status'] == 'fail':
                    raise Exception(f"Request Failed: [{resp['message']}]")
            except (aiohttp.ContentTypeError, json.JSONDecodeError):
                raise Exception('Failed to decode response as JSON')
            
            return resp

    async def get(self, **kwargs):
        log(title='PRIVATE REQUEST', type='GET', **kwargs)
        async with self._session.get(**kwargs) as response:
            try:
                text = await response.text()
                resp = json.loads(text)
                log(title='PRIVATE RESPONSE', response=resp)

                if resp['status'] == 'fail':
                    raise Exception(f"Request Failed: [{resp['message']}]")
            except (aiohttp.ContentTypeError, json.JSONDecodeError):
                raise Exception('Failed to decode response as JSON')
            
            return resp


