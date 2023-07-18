import aiohttp
import json

from threads_api.src.http_sessions.abstract_session import HTTPSession

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
    
    async def download(self, **kwargs):
        async with self._session.get(**kwargs) as response:
            return await response.read()

    async def post(self, **kwargs):
        async with self._session.post(**kwargs) as response:
            return await response.text()

    async def get(self, **kwargs):
        async with self._session.get(**kwargs) as response:
            return await response.text()


