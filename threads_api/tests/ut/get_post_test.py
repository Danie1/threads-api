from threads_api.src.threads_api import ThreadsAPI
from threads_api.src.http_sessions.abstract_session import HTTPSession

import pytest
from unittest.mock import AsyncMock, patch
import json

class HTTPSessionMock:
    def __init__(self):
        # Create MagicMock objects for each method
        self.start = AsyncMock()
        self.auth = AsyncMock()
        self.close = AsyncMock()
        self.post = AsyncMock()
        self.get = AsyncMock()
        self.download = AsyncMock()

async def refresh_public_token():
    return "asfdasdfa"

async def get_user_id_from_username(username):
    return "12345678"

@pytest.mark.asyncio
async def test_get_post(mocker):
    api = ThreadsAPI(http_session_class=HTTPSessionMock)

    mocker.patch('threads_api.src.threads_api.ThreadsAPI._refresh_public_token', side_effect=refresh_public_token)
    api._public_session.post.return_value = json.dumps({'status':'ok', 'data': {'data': {}}})
    
    await api.get_post(1234567890)
    return

@pytest.mark.asyncio
async def test_get_post_logged_in(mocker):
    api = ThreadsAPI(http_session_class=HTTPSessionMock)

    #mocker.patch('threads_api.src.threads_api.ThreadsAPI.get_user_id_from_username', side_effect=get_user_id_from_username)
    with patch.object(api, 'get_user_id_from_username', return_value="asadfasdf") as p:
        await api.login(username="", password="")

    mocker.patch('threads_api.src.threads_api.ThreadsAPI._refresh_public_token', side_effect=refresh_public_token)
    api._auth_session.get.return_value = json.dumps({'status':'ok'})

    await api.get_post(1234567890)
    return