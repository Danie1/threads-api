from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os
from threads_api.src.http_sessions.instagrapi_session import InstagrapiSession
from threads_api.src.http_sessions.requests_session import RequestsSession
from threads_api.src.http_sessions.aiohttp_session import AioHTTPSession

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

# Asynchronously posts a message
async def post(api):
    result = await api.post("Hello World!")
    
    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")

# Asynchronously posts a message
async def post_and_quote(api):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"
    post_id = await api.get_post_id_from_url(post_url)

    result = await api.post("What do you think of this?", quoted_post_id=post_id)

    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")

    
# Asynchronously posts a message with an image
async def post_include_image(api):
    result = await api.post("Hello World with an image!", image_path=".github/logo.jpg")

    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")
    
# Asynchronously posts a message with an image
async def post_include_image_from_url(api):
    result = await api.post("Hello World with an image!", image_path="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png")

    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")

# Asynchronously posts a message with an image
async def post_include_multiple_images(api):
    result = await api.post("Hello World with an image!", image_path=[".github/logo.jpg", 
                                                                      "https://upload.wikimedia.org/wikipedia/commons/b/b5/Baby.tux.sit-black-800x800.png", 
                                                                      "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"])

    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")
    

# Asynchronously posts a message with a URL
async def post_include_url(api):
    result = False
    result = await api.post("Hello World with a link!", url="https://threads.net")

    if result.media.pk:
        print(f"Post has been successfully posted with id: [{result.media.pk}]")
    else:
        print("Unable to post.")
    
# Asynchronously follows a user
async def follow_user(api):
    username_to_follow = "zuck"

    user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
    result = await api.follow_user(user_id_to_follow)

    if result:
        print(f"Successfully followed {username_to_follow}")
    else:
        print(f"Unable to follow {username_to_follow}.")
    
    

# Asynchronously unfollows a user
async def unfollow_user(api):
    username_to_follow = "zuck"
    
    user_id_to_follow = await api.get_user_id_from_username(username_to_follow)
    result = await api.unfollow_user(user_id_to_follow)

    if result:
        print(f"Successfully unfollowed {username_to_follow}")
    else:
        print(f"Unable to unfollow {username_to_follow}.")
    
async def get_user_followers(api):
    username_to_search = "zuck"
    number_of_likes_to_display = 10

    user_id_to_search = await api.get_user_id_from_username(username_to_search)
    data = await api.get_user_followers(user_id_to_search)
    
    for user in data['users'][0:number_of_likes_to_display]:
        print(f"Username: {user['username']}")

async def get_user_following(api):
    username_to_search = "zuck"
    number_of_likes_to_display = 10

    user_id_to_search = await api.get_user_id_from_username(username_to_search)
    data = await api.get_user_following(user_id_to_search)
    
    for user in data['users'][0:number_of_likes_to_display]:
        print(f"Username: {user['username']}")
    
# Asynchronously likes a post
async def like_post(api):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"
    post_id = await api.get_post_id_from_url(post_url)

    result = await api.like_post(post_id)
    
    print(f"Like status: {'Success' if result else 'Failed'}")

# Asynchronously unlikes a post
async def unlike_post(api):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"
    post_id = await api.get_post_id_from_url(post_url)

    result = await api.unlike_post(post_id)
    
    print(f"Unlike status: {'Success' if result else 'Failed'}")

# Asynchronously creates then deletes the same post
async def create_and_delete_post(api):
    post_id = await api.post("Hello World!")
    await api.delete_post(post_id)

    print(f"Created and deleted post {post_id} successfully")

# Asynchronously creates then deletes the same post
async def post_and_reply_to_post(api):
    first_post_id = await api.post("Hello World!")
    second_post_id = await api.post("Hello World to you too!", parent_post_id=first_post_id)

    print(f"Created parent post {first_post_id} and replied to it with post {second_post_id} successfully")

async def block_and_unblock_user(api):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)
    resp = await api.block_user(user_id)

    print(f"Blocking status: {'Blocked' if resp['friendship_status']['blocking'] else 'Unblocked'}")

    resp = await api.unblock_user(user_id)

    print(f"Blocking status: {'Blocked' if resp['friendship_status']['blocking'] else 'Unblocked'}")

    return

async def get_timeline(api):
    def _print_post(timeline_item):
        caption = timeline_item.thread_items[0].post.caption

        if caption == None:
            caption = "<Unable to print non-textual posts>"
        else:
            caption = caption.text
        print(f"Post -> Caption: [{caption}]\n")

    async def _print_posts_in_feed(next_max_id=None, posts_to_go=0):
        if posts_to_go > 0:
            if next_max_id is not None:
                resp = await api.get_timeline(next_max_id)
            else:
                resp = await api.get_timeline()

            
            for timeline_item in resp.items[:resp.num_results]:
                _print_post(timeline_item)

            posts_to_go -= resp.num_results
            await _print_posts_in_feed(resp.next_max_id, posts_to_go)

    await _print_posts_in_feed(posts_to_go=20)

    return

# Asynchronously gets the threads for a user
async def get_user_threads(api):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_threads(user_id)

        print(f"The threads for user '{username}' are:")
        for thread in threads.threads:
            for thread_item in thread.thread_items:
                print(f"{username}'s Post: {thread_item.post.caption.text} || Likes: {thread_item.post.like_count}")
    else:
        print(f"User ID not found for username '{username}'")

# Asynchronously gets the replies for a user
async def get_user_replies(api : ThreadsAPI):
    username = "zuck"
    user_id = await api.get_user_id_from_username(username)

    if user_id:
        threads = await api.get_user_replies(user_id)
        print(f"The replies for user '{username}' are:")
        for thread in threads.threads:
            post = thread.thread_items[0].post
            print(f"-\n{post.user.username}'s Post: {post.caption.text} || Likes: {post.like_count}")

            if len(thread.thread_items) > 1:
                first_reply = thread.thread_items[1].post
                print(f"{username}'s Reply: {first_reply.caption.text} || Likes: {first_reply.like_count}\n-")
            else:
                print(f"-> You will need to sign up / login to see more.")

    else:
        print(f"User ID not found for username '{username}'")

# Asynchronously gets a post
async def get_post(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    response = await api.get_post(post_id)

    thread = response.containing_thread.thread_items[0].post
    print(f"{thread.user.username}'s post {thread.caption.text}: || Likes: {thread.like_count}")

    for reply in response.reply_threads:
        if reply.thread_items is not None and len(reply.thread_items) >= 1:
            print(f"-\n{reply.thread_items[0].post.user.username}'s Reply: {reply.thread_items[0].post.caption.text} || Likes: {reply.thread_items[0].post.like_count}")

# Asynchronously gets the likes for a post
async def get_post_likes(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    users_list = await api.get_post_likes(post_id)
    number_of_likes_to_display = 10

    for user in users_list.users[:number_of_likes_to_display]:
        print(f'Username: {user.username} || Full Name: {user.full_name} || Follower Count: {user.follower_count} ')

# Asynchronously reposts and deletes the repost
async def repost_and_delete(api : ThreadsAPI):
    post_url = "https://www.threads.net/t/Cu0BgHESnwF"

    post_id = await api.get_post_id_from_url(post_url)
    await api.repost(post_id)
    await api.delete_repost(post_id)

# Asynchronously search users by query
async def search_user(api : ThreadsAPI):
    res = await api.search_user(query="zuck")

    index = 1
    for user in res['users']:
        print(f"#{index} -> Username:[{user['username']}] Followers: [{user['follower_count']}] Following: [{user['following_count']}]")
        index += 1

# Asynchronously gets a list of recommended users
async def get_recommended_users(api : ThreadsAPI):
    res = await api.get_recommended_users()

    index = 1
    for user in res['users']:
        print(f"#{index} -> Username:[{user['username']}] Full Name: [{user['full_name']}] Followers: [{user['follower_count']}]")
        index += 1

# Asynchronously gets a list of recommended users
async def get_notifications(api : ThreadsAPI):
    res = await api.get_notifications()

    print(res)


async def main():
    supported_http_session_classes = [AioHTTPSession, RequestsSession, InstagrapiSession]

    # Run the API calls using each of the Session types
    for http_session_class in supported_http_session_classes:
        api = ThreadsAPI(http_session_class=http_session_class)

        # Will login via REST to the Instagram API
        is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
        print(f"Login status: {'Success' if is_success else 'Failed'}")

        if is_success:
            print(f"Executing API calls using [{http_session_class}] session.")
            #await post(api) # Posts a message.
            #await post_and_quote(api) # Post a message and quote another post
            #await post_include_image(api) # Posts a message with an image.
            #await post_include_image_from_url(api) # Posts a message with an image.
            #await post_include_multiple_images(api) # Post with multiple images
            #await post_include_url(api) # Posts a message with a URL.
            #await follow_user(api) # Follows a user.
            #await unfollow_user(api) # Unfollows a user.
            #await get_user_followers(api) # Displays users who follow a given user
            #await like_post(api) # Likes a post
            #await unlike_post(api) # Unlikes a post
            #await create_and_delete_post(api) # Creates and deletes the same post
            #await post_and_reply_to_post(api) # Post and then reply to the same post
            #await block_and_unblock_user(api) # Blocks and unblocks a user 
            #await get_timeline(api) # Display items from the timeline
            #await get_user_threads(api) # Retrieves the replies made by a user.
            #await get_user_replies(api) # Retrieves the profile information of a user.
            #await get_post(api) # Retrieves a post and its associated replies.
            #await get_post_likes(api) # Get likers of a post
            #await repost_and_delete(api) # Repost a post and delete it immediately
            #await search_user(api) # Search for users by query
            #await get_recommended_users(api) # Get a list of recommended users
            #await get_notifications(api) # Get a list of notifications

        await api.close_gracefully()
     
if __name__ == "__main__":
    asyncio.run(main())