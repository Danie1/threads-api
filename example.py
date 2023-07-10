from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os

async def get_user_id_from_username():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        print(f"The user ID for username '{username}' is: {user_id}")
    else:
        print(f"User ID not found for username '{username}'")

async def get_user_profile_threads():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_profile_threads(username, user_id)
        print(f"The threads for user '{username}' are:")
        for thread in threads:
            print(f"{username}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
    else:
        print(f"User ID not found for username '{username}'")

async def get_user_profile_replies():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_profile_replies(username, user_id)
        print(f"The replies for user '{username}' are:")
        for thread in threads:
            print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

            if len(thread["thread_items"]) > 1:
                print(f"{username}'s Reply: {thread['thread_items'][1]['post']['caption']} || Likes: {thread['thread_items'][1]['post']['like_count']}\n-")
            else:
                print(f"-> You will need to sign up / login to see more.")

    else:
        print(f"User ID not found for username '{username}'")

async def get_user_profile():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        user_profile = await api.get_user_profile(username, user_id)
        print(f"User profile for '{username}':")
        print(f"Name: {user_profile['username']}")
        print(f"Bio: {user_profile['biography']}")
        print(f"Followers: {user_profile['follower_count']}")
    else:
        print(f"User ID not found for username '{username}'")

async def get_post_id_from_url():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)
    print(f"Thread post_id is {post_id}")

async def get_post():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    thread = await api.get_post(post_id)
    print(f"{thread['containing_thread']['thread_items'][0]['post']['user']['username']}'s post {thread['containing_thread']['thread_items'][0]['post']['caption']}:")

    for thread in thread["reply_threads"]:
        print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Reply: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

async def post():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        result = await api.post("Hello World!")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")

async def post_include_image():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        result = await api.post("Hello World with an image!", image_path=".github/logo.jpg")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")

async def post_include_url():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        result = await api.post("Hello World with a link!", url="https://threads.net")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")

async def follow_user():
    username_to_follow = "zuck"

    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
        result = await api.follow_user(user_id_to_follow)

    if result:
        print(f"Successfully followed {username_to_follow}")
    else:
        print(f"Unable to follow {username_to_follow}.")

async def unfollow_user():
    username_to_follow = "zuck"

    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
        result = await api.unfollow_user(user_id_to_follow)

    if result:
        print(f"Successfully unfollowed {username_to_follow}")
    else:
        print(f"Unable to unfollow {username_to_follow}.")        

'''
 Remove the # to run an individual example function wrapper.

 Each line below is standalone, and does not depend on the other.
'''
#asyncio.run(get_user_id_from_username())
#asyncio.run(get_user_profile())
#asyncio.run(get_user_profile_threads())
#asyncio.run(get_user_profile_replies())
#asyncio.run(get_post_id_from_url())
#asyncio.run(get_post())
#asyncio.run(post())
#asyncio.run(post_include_image())
#asyncio.run(post_include_url())
#asyncio.run(follow_user())
#asyncio.run(unfollow_user())