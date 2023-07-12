from ..src.threads_api import ThreadsAPI
import pytest

@pytest.mark.asyncio
async def test_get_posts_by_username():
    threads_api = ThreadsAPI()

    username = 'zuck'
    user_id = await threads_api.get_user_id_from_username(username)

    assert user_id == str(314216)

    threads = await threads_api.get_user_threads(user_id)

    assert isinstance(threads, list)