from ..src.threads_api import ThreadsAPI
import pytest

@pytest.mark.asyncio
async def test_get_posts_by_username():
    threads_api = ThreadsAPI()

    username = 'zuck'
    user_id = await threads_api.get_user_id_from_username(username)

    # TODO: This is in comment because the API for public 
    # get_user_id_from_username implementation is unstable.
    # Once this is fixed / new solutin is implemented, 
    # we can uncomment the 'assert' line
    
    #assert user_id == str(314216)

    threads = await threads_api.get_user_threads(user_id)

    assert isinstance(threads, list)