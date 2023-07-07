# [<img src="./.github/logo.jpg" width="36" height="36" />](https://github.com/junhoyeo) Threads API

[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)](https://www.npmjs.com/package/threads-api) [![MIT License](https://img.shields.io/badge/license-MIT-blue?style=flat-square&labelColor=black)](https://github.com/junhoyeo/threads-api/blob/main/license) [![Prettier Code Formatting](https://img.shields.io/badge/code_style-prettier-brightgreen.svg?style=flat-square&labelColor=black)](https://prettier.io)

> Unofficial, Reverse-Engineered Python client for Meta's [Threads](https://threads.net).

Inspired by [NPM Threads-API](https://github.com/junhoyeo/threads-api)

# Threads API - Python

Threads API is an unofficial Python client for Meta's Threads API. It allows you to interact with the API to retrieve user profile information, user IDs, and user profile threads.

Table of content:

* [Disclaimer](#disclaimer)
* [Getting started](#getting-started)
  * [How to install](#how-to-install)
  * [Initialization](#initialization)
  * [Examples](#examples)
* [API](#api)
  * [Login](#login)
  * [Get User By Username](#get-user-by-username)
  * [Get User By Identifier](#get-user-by-identifier)
  * [Get User Threads](#get-user-threads)
  * [Get User Replies](#get-user-replies)
  * [Get Post](#get-post)

## Getting Started

### 📦 Installation
```bash
pip install threads-api
```
or
```bash
poetry install threads-api
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

## 📌 Roadmap

- [x] ✅ Read public data\
  - [x] ✅ Fetch UserID(`314216`) via username(`zuck`)
  - [x] ✅ Read user profile info
  - [x] ✅ Read list of user Threads
  - [x] ✅ Read list of user Replies
  - [x] ✅ Read Post and a list of its Replies
- [ ] 🚧 Read private data
- [ ] 🚧 Write data (i.e. write automated Threads)
- [ ]🚧  CI/CD
  - [ ]🚧  Pytest
  - [ ]🚧  GitHub Actions Pipeline


# License
This project is licensed under the MIT license.