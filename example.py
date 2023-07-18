from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os
import logging
from threads_api.src.http_sessions.instagrapi_session import InstagrapiSession
from threads_api.src.http_sessions.requests_session import RequestsSession
from threads_api.src.http_sessions.aiohttp_session import AioHTTPSession

# Asynchronously gets the user ID from a username
async def get_user_id_from_username():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        print(f"The user ID for username '{username}' is: {user_id}")
    else:
        print(f"User ID not found for username '{username}'")
    
    await api.close_gracefully()

# Asynchronously gets the threads for a user
async def get_user_threads():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_threads(user_id)
        print(f"The threads for user '{username}' are:")
        for thread in threads:
            print(f"{username}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
    else:
        print(f"User ID not found for username '{username}'")
    
    await api.close_gracefully()

# Asynchronously gets the replies for a user
async def get_user_replies():
    api = ThreadsAPI()

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

    await api.close_gracefully()


# Asynchronously gets the user profile
async def get_user_profile():
    api = ThreadsAPI()

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

    await api.close_gracefully()

# Asynchronously gets the post ID from a URL
async def get_post_id_from_url():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)
    print(f"Thread post_id is {post_id}")

    await api.close_gracefully()

# Asynchronously gets a post
async def get_post():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    thread = await api.get_post(post_id)
    print(f"{thread['containing_thread']['thread_items'][0]['post']['user']['username']}'s post {thread['containing_thread']['thread_items'][0]['post']['caption']}:")

    for thread in thread["reply_threads"]:
        print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Reply: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

    await api.close_gracefully()

# Asynchronously gets the likes for a post
async def get_post_likes():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    likes = await api.get_post_likes(post_id)
    number_of_likes_to_display = 10

    for user_info in likes[:number_of_likes_to_display]:
        print(f'Username: {user_info["username"]} || Full Name: {user_info["full_name"]} || Follower Count: {user_info["follower_count"]} ')

    await api.close_gracefully()

# Asynchronously posts a message
async def post():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        result = await api.post("Hello World!")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")

    await api.close_gracefully()

# Asynchronously posts a message with an image
async def post_include_image():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        result = await api.post("Hello World with an image!", image_path=".github/logo.jpg")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")
    
    await api.close_gracefully()

# Asynchronously posts a message with an image
async def post_include_image_from_url():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        result = await api.post("Hello World with an image!", image_path="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")
    
    await api.close_gracefully()

# Asynchronously posts a message with a URL
async def post_include_url():
    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        result = await api.post("Hello World with a link!", url="https://threads.net")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")
    
    await api.close_gracefully()

# Asynchronously follows a user
async def follow_user():
    username_to_follow = "zuck"

    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
        result = await api.follow_user(user_id_to_follow)

    if result:
        print(f"Successfully followed {username_to_follow}")
    else:
        print(f"Unable to follow {username_to_follow}.")
    
    await api.close_gracefully()

# Asynchronously unfollows a user
async def unfollow_user():
    username_to_follow = "zuck"

    api = ThreadsAPI()
    is_success = await api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    result = False
    if is_success:
        user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
        result = await api.unfollow_user(user_id_to_follow)

    if result:
        print(f"Successfully unfollowed {username_to_follow}")
    else:
        print(f"Unable to unfollow {username_to_follow}.")
    
    await api.close_gracefully()

# Code example of logging in while storing token encrypted on the file-system
async def login_with_cache():

    local_cache_path = ".token"

    api1 = ThreadsAPI()
    
    # Will login via REST to the Instagram API
    is_success = await api1.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=local_cache_path)
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    await api1.close_gracefully()

    api2 = ThreadsAPI()

    # Decrypts the token from the .token file using the password as the key.
    # This reduces the number of login API calls, to the bare minimum
    is_success = await api2.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=local_cache_path)
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    await api2.close_gracefully()

async def get_user_followers():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        username_to_search = "zuck"
        number_of_likes_to_display = 10

        user_id_to_search = await api.get_user_id_from_username(username_to_search)
        data = await api.get_user_followers(user_id_to_search)
        
        for user in data['users'][0:number_of_likes_to_display]:
            print(f"Username: {user['username']}")

    await api.close_gracefully()

async def get_user_following():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        username_to_search = "zuck"
        number_of_likes_to_display = 10

        user_id_to_search = await api.get_user_id_from_username(username_to_search)
        data = await api.get_user_following(user_id_to_search)
        
        for user in data['users'][0:number_of_likes_to_display]:
            print(f"Username: {user['username']}")
    
    await api.close_gracefully()

# Asynchronously likes a post
async def like_post():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        post_url = "https://www.threads.net/t/CuZsgfWLyiI"
        post_id = await api.get_post_id_from_url(post_url)

        result = await api.like_post(post_id)
        
        print(f"Like status: {'Success' if result else 'Failed'}")

    await api.close_gracefully()

# Asynchronously unlikes a post
async def unlike_post():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        post_url = "https://www.threads.net/t/CuZsgfWLyiI"
        post_id = await api.get_post_id_from_url(post_url)

        result = await api.unlike_post(post_id)
        
        print(f"Unlike status: {'Success' if result else 'Failed'}")

    await api.close_gracefully()

# Asynchronously creates then deletes the same post
async def create_and_delete_post():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        post_id = await api.post("Hello World!")
        await api.delete_post(post_id)

        print(f"Created and deleted post {post_id} successfully")

    await api.close_gracefully()

# Asynchronously creates then deletes the same post
async def post_and_reply_to_post():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        first_post_id = await api.post("Hello World!")
        second_post_id = await api.post("Hello World to you too!", parent_post_id=first_post_id)

        print(f"Created parent post {first_post_id} and replied to it with post {second_post_id} successfully")

    await api.close_gracefully()

async def block_and_unblock_user():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        username = "zuck"
        user_id = await api.get_user_id_from_username(username)
        resp = await api.block_user(user_id)

        print(f"Blocking status: {'Blocked' if resp['friendship_status']['blocking'] else 'Unblocked'}")

        resp = await api.unblock_user(user_id)

        print(f"Blocking status: {'Blocked' if resp['friendship_status']['blocking'] else 'Unblocked'}")

    await api.close_gracefully()

    return

async def get_timeline():
    api = ThreadsAPI()

    def _print_post(post):
        caption = post['thread_items'][0]['post']['caption']

        if caption == None:
            caption = "<Unable to print non-textual posts>"
        else:
            caption = caption['text']
        print(f"Post -> Caption: [{caption}]\n")

    async def _print_posts_in_feed(next_max_id=None, posts_to_go=0):
        if posts_to_go > 0:
            if next_max_id is not None:
                resp = await api.get_timeline(next_max_id)
            else:
                resp = await api.get_timeline()

            for post in resp['items'][:resp['num_results']]:
                _print_post(post)

            posts_to_go -= resp['num_results']
            await _print_posts_in_feed(resp['next_max_id'], posts_to_go)


    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        await _print_posts_in_feed(posts_to_go=20)
        
    await api.close_gracefully()

    return

async def get_timeline_with_api(api=ThreadsAPI()):
    def _print_post(post):
        caption = post['thread_items'][0]['post']['caption']

        if caption == None:
            caption = "<Unable to print non-textual posts>"
        else:
            caption = caption['text']
        print(f"Post -> Caption: [{caption}]\n")

    async def _print_posts_in_feed(next_max_id=None, posts_to_go=0):
        if posts_to_go > 0:
            if next_max_id is not None:
                resp = await api.get_timeline(next_max_id)
            else:
                resp = await api.get_timeline()

            for post in resp['items'][:resp['num_results']]:
                _print_post(post)

            posts_to_go -= resp['num_results']
            await _print_posts_in_feed(resp['next_max_id'], posts_to_go)


    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        await _print_posts_in_feed(posts_to_go=20)
        
    await api.close_gracefully()

    return

# Asynchronously gets the threads for a user
async def get_user_threads_while_authenticated():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        if user_id:
            resp = await api.get_user_threads(user_id)
            print(f"The threads for user '{username}' are:")
            for thread in resp['threads']:
                print(f"{username}'s Post: {thread['thread_items'][0]['post']['caption']['text']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
        else:
            print(f"User ID not found for username '{username}'")

    await api.close_gracefully()

# Asynchronously gets the replies for a user
async def get_user_replies_while_authenticated():
    api = ThreadsAPI()

    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        if user_id:
            threads = await api.get_user_replies(user_id)
            print(f"The replies for user '{username}' are:")
            for thread in threads['threads']:
                print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Post: {thread['thread_items'][0]['post']['caption']['text']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

                print(f"{username}'s Reply: {thread['thread_items'][1]['post']['caption']['text']} || Likes: {thread['thread_items'][1]['post']['like_count']}\n-")
    else:
        print(f"User ID not found for username '{username}'")
    
    await api.close_gracefully()

'''
 Remove the # to run an individual example function wrapper.

 Each line below is standalone, and does not depend on the other.
'''
##### Do not require login #####

#asyncio.run(get_user_id_from_username()) # Retrieves the user ID for a given username.
#asyncio.run(get_user_profile()) # Retrieves the threads associated with a user.
#asyncio.run(get_user_threads()) # Retrieves the replies made by a user.
#asyncio.run(get_user_replies()) # Retrieves the profile information of a user.
#asyncio.run(get_post_id_from_url()) # Retrieves the post ID from a given URL.
#asyncio.run(get_post()) # Retrieves a post and its associated replies.
#asyncio.run(get_post_likes()) # Retrieves the likes for a post.

##### Require login (included) #####

#asyncio.run(post()) # Posts a message.
#asyncio.run(post_include_image()) # Posts a message with an image.
#asyncio.run(post_include_image_from_url()) # Posts a message with an image.
#asyncio.run(post_include_url()) # Posts a message with a URL.
#asyncio.run(follow_user()) # Follows a user.
#asyncio.run(unfollow_user()) # Unfollows a user.
#asyncio.run(login_with_cache()) # Displays token cache capability
#asyncio.run(get_user_followers()) # Displays users who follow a given user
#asyncio.run(like_post()) # Likes a post
#asyncio.run(unlike_post()) # Unlikes a post
#asyncio.run(create_and_delete_post()) # Creates and deletes the same post
#asyncio.run(post_and_reply_to_post()) # Post and then reply to the same post
#asyncio.run(block_and_unblock_user()) # Blocks and unblocks a user 
#asyncio.run(get_timeline()) # Display items from the timeline
#asyncio.run(get_user_threads_while_authenticated()) # Retrieves the replies made by a user.
#asyncio.run(get_user_replies_while_authenticated()) # Retrieves the profile information of a user.

#asyncio.run(get_timeline_with_api(ThreadsAPI(http_session_class=AioHTTPSession))) # Use aiohttp session under the hood
#asyncio.run(get_timeline_with_api(ThreadsAPI(http_session_class=RequestsSession))) # Use requests session under the hood
#asyncio.run(get_timeline_with_api(ThreadsAPI(http_session_class=InstagrapiSession))) # Use instagrapi session under the hood