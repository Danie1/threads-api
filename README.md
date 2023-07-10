# [<img src="https://raw.githubusercontent.com/danie1/threads-api/main/.github/logo.jpg" width="36" height="36" />](https://github.com/danie1) Meta's Threads.net API

[![Downdloads](https://pepy.tech/badge/threads-api)](https://pypi.org/project/threads-api/)
[![Version](https://img.shields.io/pypi/v/threads-api.svg?style=flat)](https://pypi.org/project/threads-api/)
[![Python](https://img.shields.io/pypi/pyversions/threads-api.svg)](https://pypi.org/project/threads-api/) [![MIT License](https://img.shields.io/pypi/l/threads-api.svg?style=flat)](https://github.com/Danie1/threads-api/blob/main/LICENSE) 

> Unofficial, Reverse-Engineered Python client for Meta's [Threads](https://threads.net).

Inspired by [NPM Threads-API](https://github.com/junhoyeo/threads-api)

# Threads API - Python

Threads API is an unofficial Python client for Meta's Threads API. It allows you to interact with the API to login, post, retrieve user profile information, user IDs and user profile threads.

Table of content:

* [Demo](#demo)
* [Getting started](#getting-started)
  * [Installation](#Installation)
* [Usage Examples](#usage-examples)
* [Roadmap](#📌-roadmap)
* [License](#license)

# Demo
<img src=".github/user_example1.jpeg" alt="drawing" width="500"/>


## Getting Started

### 📦 Installation
```bash
pip install threads-api
```
or
```bash
poetry install threads-api
```

Example using threads-api to post to Threads.net:
``` python
from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def post():
    threads_api = ThreadsAPI()
    await threads_api.login(os.environ.get('USERNAME'), os.environ,get('PASSWORD'))
    result = await threads_api.post("I am posting this from the threads api!")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")

async def main():
    await post()

# Create an event loop and run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Usage Examples
<details>
  <summary>"get_user_id_from_username" Function</summary>

``` python
from threads_api.src.threads_api import ThreadsAPI
import asyncio

async def get_user_id_from_username():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        print(f"The user ID for username '{username}' is: {user_id}")
    else:
        print(f"User ID not found for username '{username}'")
```

Example Output:
```
The user ID for username 'zuck' is: 314216
```
</details>

<details>
  <summary>"get_user_profile" Function</summary>

``` python
async def get_user_profile():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        user_profile = await threads_api.get_user_profile(username, user_id)
        print(f"User profile for '{username}':")
        print(f"Name: {user_profile['username']}")
        print(f"Bio: {user_profile['biography']}")
        print(f"Followers: {user_profile['follower_count']}")
    else:
        print(f"User ID not found for username '{username}'")
```

Example Output:
```
User profile for 'zuck':
Name: zuck
Bio: 
Followers: 2288633
```
</details>

<details>
  <summary>"get_user_profile_threads" Function</summary>

``` python
async def get_user_profile_threads():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        threads = await threads_api.get_user_profile_threads(username, user_id)
        print(f"The threads for user '{username}' are:")
        for thread in threads:
            print(f"Text: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
    else:
        print(f"User ID not found for username '{username}'")

```

Example Output:
```
The threads for user 'zuck' are:
zuck's Post: {'text': '70 million sign ups on Threads as of this morning. Way beyond our expectations.'} || Likes: 159293
zuck's Post: {'text': 'Lots of work on basic capabilities this morning.'} || Likes: 217148
zuck's Post: {'text': "Wow, 30 million sign ups as of this morning. Feels like the beginning of something special, but we've got a lot of work ahead to build out the app."} || Likes: 340098
zuck's Post: {'text': '10 million sign ups in seven hours 🤯'} || Likes: 357105
zuck's Post: {'text': 'Just passed 5 million sign ups in the first four hours...'} || Likes: 156277
zuck's Post: {'text': 'Threads just passed 2 million sign ups in the first two hours.'} || Likes: 132504
zuck's Post: {'text': "Glad you're all here on day one. Let's build something great together!"} || Likes: 175563
zuck's Post: {'text': "Let's do this. Welcome to Threads. 🔥"} || Likes: 166987
```
</details>


<details>
  <summary>"get_user_profile_replies" Function</summary>

``` python
async def get_user_profile_replies():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        threads = await threads_api.get_user_profile_replies(username, user_id)
        print(f"The replies for user '{username}' are:")
        for thread in threads:
            print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")

            if len(thread["thread_items"]) > 1:
                print(f"{username}'s Reply: {thread['thread_items'][1]['post']['caption']} || Likes: {thread['thread_items'][1]['post']['like_count']}\n-")
            else:
                print(f"-> You will need to sign up / login to see more.")

    else:
        print(f"User ID not found for username '{username}'")

```

Example Output:
```
mosseri's Post: {'text': 'I joined Meta, then Facebook, 15 years ago today. We were four years old, had ~450 employees, had just translated the site, and had ~70M people.\n\nToday we hit that many signups on Threads. Now signups and retained users are different, and we built Threads on top of an amazing foundation provided by Instagram and by Meta, but there is something elegant about that symmetry.\n\nThank you to the team that actually built this app, thank you to the company and @zuck for trusting me all these years, 🙏🏼'} || Likes: 25523
zuck's Reply: {'text': "Congrats! Great milestone to celebrate 15 years. I'm grateful for everything you do."} || Likes: 5506
-
-
adidas's Post: {'text': 'to sock and slide or not to sock and slide today…'} || Likes: 7425
zuck's Reply: {'text': 'No socks for life'} || Likes: 9976
-
-
evachen212's Post: {'text': 'This is a good first Thread 🙌🏼'} || Likes: 8739
zuck's Reply: {'text': 'Believe when I say, I want it that way.'} || Likes: 23991
-
-
iamsamyrlaine's Post: {'text': "Can't remember the last time I even had the Twitter app on my phone, let alone posted something there; I'm definitely down with Threads though!"} || Likes: 4876
zuck's Reply: {'text': '🙌'} || Likes: 7928

...
```
</details>

<details>
  <summary>"get_post_id_from_url" Function</summary>

``` python
async def get_post_id_from_url():
    threads_api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await threads_api.get_post_id_from_url(post_url)
    print(f"'Thread post {post_id}':")

```

Example Output:
```
Thread post_id is 3141737961795561608
```
</details>

<details>
  <summary>"get_post" Function</summary>

``` python
async def get_post():
    threads_api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await threads_api.get_post_id_from_url(post_url)

    thread = await threads_api.get_post(post_id)
    print(f"'Thread post {thread['containing_thread']['thread_items'][0]['post']['caption']}':")

    for thread in thread["reply_threads"]:
        print(f"-\n{thread['thread_items'][0]['post']['user']['username']}'s Post: {thread['thread_items'][0]['post']['caption']} || Likes: {thread['thread_items'][0]['post']['like_count']}")
```

Example Output:
```
zuck's post {'text': '70 million sign ups on Threads as of this morning. Way beyond our expectations.'}:
-
luclevesque's Reply: {'text': 'Wow 🤯'} || Likes: 167
-
jasminericegirl's Reply: {'text': 'you are doing amazing sweetie'} || Likes: 391
-
zhra.ghalenoei's Reply: {'text': 'نصفشون ایرانین یَره🤣'} || Likes: 0
-
a.llisterthomas's Reply: {'text': 'elon finna drop this guy😭🥊'} || Likes: 0
-
_vormund_'s Reply: None || Likes: 0
-
sri_ty_'s Reply: {'text': '🐸So nice'} || Likes: 0
-
_william.carrera_'s Reply: {'text': 'Where’s the porn here Mr Zuck'} || Likes: 0
-
kal_blogs's Reply: {'text': 'When you said ‘our’, was it the ‘royal our’?'} || Likes: 0
-
nasheet's Reply: {'text': 'That is crazy road to 100M'} || Likes: 19
-
dsb.don's Reply: {'text': 'You did it 🇰🇪♥️'} || Likes: 0
-
pisceansoulx's Reply: {'text': 'Wohoo. You the man Zucker'} || Likes: 0
-
winchester_757's Reply: {'text': 'If only the meta verse was this good LMAO'} || Likes: 0
-
winchester_757's Reply: {'text': 'Only 10 mil more to match the big guy'} || Likes: 0
```
</details>

<details>
  <summary>"post" Function</summary>

``` python
async def post():
    threads_api = ThreadsAPI()
    # either set USERNAME and PASSWORD as environment variables, or replace these with your actual credentials
    await threads_api.login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    result = await threads_api.post("Hello World!")

    if result:
        print("Post has been successfully posted")
    else:
        print("Unable to post.")
```

Example Output:
```
Post has been successfully posted
```
</details>

## 📌 Roadmap

- [x] ✅ Login as User
- [x] ✅ Write Posts
  - [x] ✅ Posts with just text
  - [x] ✅ Posts with text and an image
  - [x] ✅ Posts with text that share a url
- [x] ✅ Perform Actions
  - [x] ✅ Like Posts
  - [x] ✅ Unlike Posts
  - [x] ✅ Follow User
  - [x] ✅ Unfollow User
- [x] ✅ Read Data\
  - [x] ✅ Read a user_id (eg. `314216`) via username(eg. `zuck`)
  - [x] ✅ Read user profile info
  - [x] ✅ Read list of user Threads
  - [x] ✅ Read list of user Replies
  - [x] ✅ Read Post and a list of its Replies
- [ ] 🚧  Upload images and videos
- [ ] 🚧  Reply to Posts
- [x] ✅  CI/CD
  - [ ] 🚧  Pytest
  - [x] ✅  GitHub Actions Pipeline


# License
This project is licensed under the MIT license.