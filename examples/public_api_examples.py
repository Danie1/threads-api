from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os
import logging
from threads_api.src.http_sessions.instagrapi_session import InstagrapiSession
from threads_api.src.http_sessions.requests_session import RequestsSession
from threads_api.src.http_sessions.aiohttp_session import AioHTTPSession

from threads_api.src.anotherlogger import format_log

# Asynchronously gets the user ID from a username
async def get_user_id_from_username(api : ThreadsAPI):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        print(f"The user ID for username '{username}' is: {user_id}")
    else:
        print(f"User ID not found for username '{username}'")
    
# Asynchronously gets the threads for a user
async def get_user_threads(api : ThreadsAPI):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_threads(user_id)
        print(f"The threads for user '{username}' are:")
        for thread in threads:
            print(f"{username}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
    else:
        print(f"User ID not found for username '{username}'")
    
# Asynchronously gets the replies for a user
async def get_user_replies(api : ThreadsAPI):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_replies(user_id)
        print(f"The replies for user '{username}' are:")
        for thread in threads:
            print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

            if len(thread["thread_items"]) > 1:
                print(f"{username}'s Reply: {thread['thread_items'][1]['post']['caption']} || Likes: {thread['thread_items'][1]['post']['like_count']}\n-")
            else:
                print(f"-> You will need to sign up / login to see more.")

    else:
        print(f"User ID not found for username '{username}'")

# Asynchronously gets the user profile
async def get_user_profile(api : ThreadsAPI):

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        user_profile = await api.get_user_profile(user_id)
        print(f"User profile for '{username}':")
        print(f"Name: {user_profile['username']}")
        print(f"Bio: {user_profile['biography']}")
        print(f"Followers: {user_profile['follower_count']}")
    else:
        print(f"User ID not found for username '{username}'")

# Asynchronously gets the post ID from a URL
async def get_post_id_from_url(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)
    print(f"Thread post_id is {post_id}")

# Asynchronously gets a post
async def get_post(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    thread = await api.get_post(post_id)
    print(f"{thread['containing_thread']['thread_items'][0]['post']['user']['username']}'s post {thread['containing_thread']['thread_items'][0]['post']['caption']}:")

    for thread in thread["reply_threads"]:
        if 'thread_items' in thread and len(thread['thread_items']) > 1:
            print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Reply: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

# Asynchronously gets the likes for a post
async def get_post_likes(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    likes = await api.get_post_likes(post_id)
    number_of_likes_to_display = 10

    for user_info in likes[:number_of_likes_to_display]:
        print(f'Username: {user_info["username"]} || Full Name: {user_info["full_name"]} || Follower Count: {user_info["follower_count"]} ')

'''
 Remove the # to run an individual example function wrapper.

 Each line below is standalone, and does not depend on the other.
'''
##### Do not require login #####

async def main():
    supported_http_session_classes = [AioHTTPSession, RequestsSession, InstagrapiSession]

    # Run the API calls using each of the Session types
    for http_session_class in supported_http_session_classes:
        api = ThreadsAPI(http_session_class=http_session_class)

        print(f"Executing API calls using [{http_session_class}] session.")
        #await get_user_id_from_username(api) # Retrieves the user ID for a given username.
        #await get_user_profile(api) # Retrieves the threads associated with a user.
        #await get_user_threads(api) # Retrieves the replies made by a user.
        #await get_user_replies(api) # Retrieves the profile information of a user.
        #await get_post_id_from_url(api) # Retrieves the post ID from a given URL.
        #await get_post(api) # Retrieves a post and its associated replies.
        #await get_post_likes(api) # Retrieves the likes for a post.

        await api.close_gracefully()

if __name__ == "__main__":
    asyncio.run(main())
