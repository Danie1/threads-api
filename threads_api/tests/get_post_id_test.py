from ..src.threads_api import ThreadsAPI
import pytest

@pytest.mark.asyncio
async def test_get_post_id_from_url():
    threads_api = ThreadsAPI()

    url = "https://www.threads.net/t/Cumq_jaMsC1"
    post__id = await threads_api.get_post_id_from_url(url)

    assert post__id == str(3145390475065868469)