# [<img src="https://raw.githubusercontent.com/danie1/threads-api/main/.github/logo.jpg" width="36" height="36" />](https://github.com/danie1) Meta's Threads.net API

[![Downdloads](https://pepy.tech/badge/threads-api)](https://pypi.org/project/threads-api/)
[![Version](https://img.shields.io/pypi/v/threads-api.svg?style=flat)](https://pypi.org/project/threads-api/)
[![Python](https://img.shields.io/pypi/pyversions/threads-api.svg)](https://pypi.org/project/threads-api/) [![MIT License](https://img.shields.io/pypi/l/threads-api.svg?style=flat)](https://github.com/Danie1/threads-api/blob/main/LICENSE) 

> Unofficial, Reverse-Engineered Python client for Meta's [Threads](https://threads.net).

Inspired by [NPM Threads-API](https://github.com/junhoyeo/threads-api)

# Threads API - Python

Threads API is an unofficial Python client for Meta's Threads API. It allows you to interact with the API to login, read and publish posts, view who liked a post, retrieve user profile information, follow/unfollow and much more.

It is built using `aiohttp` to ease asynchronous execution of the API, for ⚡ super-fast ⚡ results.

> Note: Since v1.1.3 we are using ```instagrapi``` package to login.

Table of content:

* [Demo](#demo)
* [Getting started](#getting-started)
  * [Installation](#installation)
  * [Set Log Level](#set-desired-log-level)
* [Contributions](#contributing-to-danie1threads-api)
* [Supported Features](#supported-features)
* [Usage Examples](#usage-examples)
* [Roadmap](#📌-roadmap)
* [License](#license)

# Demo
<img src="https://raw.githubusercontent.com/Danie1/threads-api/main/.github/user_example2.jpg" alt="drawing" width="500"/>

## Getting Started

### 📦 Installation
```bash
pip install threads-api
```
or
```bash
poetry add threads-api
```

Example using threads-api to post to Threads.net:
``` python
from threads_api.src.threads_api import ThreadsAPI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def post():
    api = ThreadsAPI()
    await api.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'), cached_token_path=".token")
    result = await api.post(caption="Posting this from the Danie1/threads-api!", image_path=".github/logo.jpg")


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
## Set Desired Log Level
Threads-API reads the environment variable ```LOG_LEVEL``` and sets the log-level according to its value.

Possible values include: ```DEBUG, INFO, WARNING, ERROR, CRITICAL```

**Log Level defaults to WARNING when not set.**

Useful to know:
``` bash
# Set Info (Prints general flow)
export LOG_LEVEL=INFO
```

``` bash
# Set Debug (Prints HTTP Requests + HTTP Responses)
export LOG_LEVEL=DEBUG
```

# Contributing to Danie1/threads-api
## Getting Started

With Poetry (*Recommended*)
``` bash
# Step 1: Clone the project
git clone git@github.com:Danie1/threads-api.git

# Step 2: Install dependencies to virtual environment
poetry install

# Step 3: Activate virtual environment
poetry shell
```
or

Without Poetry

``` bash
# Step 1: Clone the project
git clone git@github.com:Danie1/threads-api.git

# Step 2: Create virtual environment
python3 -m venv env

# Step 3 (Unix/MacOS): Activate virtual environment
source env/bin/activate # Unix/MacOS

# Step 3 (Windows): Activate virtual environment
.\env\Scripts\activate # Windows

# Step 4: Install dependencies
pip install -r requirements.txt
```


# Supported Features
- [x] ✅ Login functionality, including 2FA 🔒
  - [x] ✅ Cache login token securely (reduce login requests / due to restrictive limits)
- [x] ✅ Write Posts (Requires Login 🔒)
  - [x] ✅ Posts with just text
  - [x] ✅ Posts with text and an image
  - [x] ✅ Posts with text that share a url
  - [x] ✅ Reply to Posts
- [x] ✅ Perform Actions (Requires Login 🔒)
  - [x] ✅ Like Posts
  - [x] ✅ Unlike Posts
  - [x] ✅ Delete post
  - [x] ✅ Follow User
  - [x] ✅ Unfollow User
  - [x] ✅ Block User
  - [x] ✅ Unblock User
  - [x] ✅ Restrict User
  - [x] ✅ Unrestrict User
  - [x] ✅ Mute User
  - [x] ✅ Unmute User
- [x] ✅ Read Public Data
  - [x] ✅ Read a user_id (eg. `314216`) via username(eg. `zuck`)
  - [x] ✅ Read a user's profile info
  - [x] ✅ Read list of a user's Threads
  - [x] ✅ Read list of a user's Replies
  - [x] ✅ Read Post and a list of its Replies
  - [x] ✅ View who liked a post
- [x] ✅ Read Private Data (Requires Login 🔒)
  - [x] ✅ Read a user's followers list
  - [x] ✅ Read a user's following list
- [x] ✅  CI/CD
  - [x] ✅  GitHub Actions Pipeline

## Usage Examples
View [example.py](https://github.com/Danie1/threads-api/blob/main/example.py) for code examples. 
At the end of the file you will be able to uncomment and run the individual examples with ease.

Then simply run as:
```
# Pass the credentials as environment variables
USERNAME=<Instagram Username> PASSWORD=<Instagram Password> python3 example.py
```

### Samples

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
        user_profile = await threads_api.get_user_profile(user_id)
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
  <summary>"get_user_threads" Function</summary>

``` python
async def get_user_threads():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        threads = await threads_api.get_user_threads(user_id)
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
  <summary>"get_user_replies" Function</summary>

``` python
async def get_user_replies():
    threads_api = ThreadsAPI()

    username = "zuck"
    user_id = await threads_api.get_user_id_from_username(username)

    if user_id:
        threads = await threads_api.get_user_replies(user_id)
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
  <summary>"get_post_likes" Function</summary>

``` python
async def get_post_likes():
    api = ThreadsAPI()
    post_url = "https://www.threads.net/t/CuZsgfWLyiI"

    post_id = await api.get_post_id_from_url(post_url)

    likes = await api.get_post_likes(post_id)
    number_of_likes_to_display = 10

    for user_info in likes[:number_of_likes_to_display]:
        print(f'Username: {user_info["username"]} || Full Name: {user_info["full_name"]} || Follower Count: {user_info["follower_count"]} ')
```

Example Output:
```
Username: andrew_votava || Full Name: Andrew Votava || Follower Count: 19 
Username: herson_theeog || Full Name: Herson_theeOG || Follower Count: 323 
Username: dhruv___kanojia || Full Name: Dhruv🌟 || Follower Count: 38 
Username: codecrusadepk || Full Name: Code Crusade || Follower Count: 9 
Username: toxicated_jeshim_007 || Full Name: Jeshim Akhtar Choudhury || Follower Count: 6 
Username: jay.rex.official || Full Name: Jay Rex || Follower Count: 30 
Username: jessy.servin || Full Name: Jessica Servín || Follower Count: 343 
Username: joshxmadrid || Full Name: Josh Madrid || Follower Count: 1092 
Username: ganjipro || Full Name: Song Ganji || Follower Count: 1649 
Username: bilalmuhamadi || Full Name: B I L A L  M U H A M A D I || Follower Count: 111 
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
- [ ] 🚧 Read feed, notifications
- [ ] 🚧 Post text and share a video
- [ ] 🚧 Documentation Improvements
- [ ] 🚧 CI/CD Improvements
  - [ ] 🚧 Add coverage Pytest


# License
This project is licensed under the MIT license.
