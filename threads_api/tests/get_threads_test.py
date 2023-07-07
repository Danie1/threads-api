from ..src.threads_api import ThreadsAPI
import pytest

@pytest.mark.asyncio
async def test_get_posts_by_username():
    threads_api = ThreadsAPI()

    username = 'zuck'
    id = await threads_api.get_user_id_from_username(username)

    if not id:
        return
    assert isinstance(id, str)

    threads = await threads_api.get_user_profile_threads(username, id)
    assert isinstance(threads, list)