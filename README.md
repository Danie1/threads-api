> As of October 1st 2023 this repository is archived, and no longer be maintained. 
---

# [<img src="https://raw.githubusercontent.com/danie1/threads-api/main/.github/logo.jpg" width="36" height="36" />](https://github.com/danie1) Meta's Threads.net API



[![Downdloads](https://pepy.tech/badge/threads-api)](https://pypi.org/project/threads-api/)
[![Version](https://img.shields.io/pypi/v/threads-api.svg?style=flat)](https://pypi.org/project/threads-api/)
[![Releases](https://img.shields.io/github/v/release/danie1/threads-api.svg)](https://github.com/danie1/threads-api/releases)
[![Python](https://img.shields.io/pypi/pyversions/threads-api.svg)](https://pypi.org/project/threads-api/) [![MIT License](https://img.shields.io/pypi/l/threads-api.svg?style=flat)](https://github.com/Danie1/threads-api/blob/main/LICENSE) 

[![Workflow Status](https://github.com/Danie1/threads-api/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Danie1/threads-api/actions/workflows/python-tests.yml)



> Unofficial, Reverse-Engineered Python client for Meta's [Threads](https://threads.net).

Inspired by [NPM Threads-API](https://github.com/junhoyeo/threads-api)

# Threads API - Python

Threads API is an unofficial Python client for Meta's Threads API. It allows you to interact with the API to login, read and publish posts, view who liked a post, retrieve user profile information, follow/unfollow and much more.

✅ Configurable underlying HTTP Client (`aiohttp` / `requests` / `instagrapi`'s client / implement your own)

✅ Authentication Methods supported via `instagrapi`

✅ Stores token and settings locally, to reduce login-attempts (*uses the same token for all authenticated requests for up to 24 hrs*)

✅ Pydantic structures for API responses (for IDE auto-completion) (at [types.py](https://github.com/Danie1/threads-api/blob/main/threads_api/src/types.py))

✅ Actively Maintained since Threads.net Release (responsive in Github Issues, try it out!)



> **Important Tip** Use the same `cached_token_path` for connections, to reduce the number of actual login attempts. When needed, threads-api will reconnect and update the file in `cached_token_path`.  

Table of content:

* [Demo](#demo)
* [Getting started](#getting-started)
  * [Installation](#installation)
  * [Set Log Level & Troubleshooting](#set-desired-log-level)
  * [Set HTTP Client](#choose-a-different-http-client)
* [Supported Features](#supported-features)
* [Usage Examples](#usage-examples)
* [Roadmap](#📌-roadmap)
* [Contributions](#contributing-to-danie1threads-api)
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
    
    await api.close_gracefully()
    

async def main():
    await post()

# Run the main function
asyncio.run(main())
```

## Customize HTTP Client
Each HTTP client brings to the table different functionality. Use whichever you like, or implement your own wrapper.

Usage:
``` python
api = ThreadsAPI(http_session_class=AioHTTPSession) # default
# or
api = ThreadsAPI(http_session_class=RequestsSession)
# or
api = ThreadsAPI(http_session_class=InstagrapiSession)
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

<details>
  <summary>Example of Request when LOG_LEVEL=DEBUG</summary>

``` bash
<---- START ---->
Keyword arguments:
  [title]: ["PUBLIC REQUEST"]
  [type]: ["GET"]
  [url]: ["https://www.instagram.com/instagram"]
  [headers]: [{
    "Authority": "www.threads.net",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.threads.net",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "X-ASBD-ID": "129477",
    "X-IG-App-ID": "238260118697367"
}]
<---- END ---->

```

</details>

### Troubleshooting threads-api
Upon unexpected error, or upon receiving an exception with:  `Oops, this is an error that hasn't yet been properly handled.\nPlease open an issue on Github at https://github.com/Danie1/threads-api.`

Please open a Github Issue with all of the information you can provide, which includes the last Request and Response (Set `LOG_LEVEL=DEBUG`)

# Supported Features
- [x] ✅ Pydantic typing API responses at [types.py](https://github.com/Danie1/threads-api/blob/main/threads_api/src/types.py)
- [x] ✅ Login functionality, including 2FA 🔒
  - [x] ✅ Cache login token securely (reduce login requests / due to restrictive limits)
  - [x] ✅ Saves settings locally, such as device information and timezone to use along your sessions
- [x] ✅ Read recommended posts from timeline (Requires Login 🔒)
- [x] ✅ Write Posts (Requires Login 🔒)
  - [x] ✅ Posts with just text
  - [x] ✅ Posts and quote another post
  - [x] ✅ Posts with text and an image
  - [x] ✅ Posts with text and multiple images
  - [x] ✅ Posts with text that shares a url
  - [x] ✅ Repost a post
  - [x] ✅ Reply to Posts
- [x] ✅ Perform Actions (Requires Login 🔒)
  - [x] ✅ Like Posts
  - [x] ✅ Unlike Posts
  - [x] ✅ Delete post
  - [x] ✅ Delete repost
  - [x] ✅ Follow User
  - [x] ✅ Unfollow User
  - [x] ✅ Block User
  - [x] ✅ Unblock User
  - [x] ✅ Restrict User
  - [x] ✅ Unrestrict User
  - [x] ✅ Mute User
  - [x] ✅ Unmute User
  - [x] ✅ Search for users
  - [x] ✅ Get Recommended Users
  - [x] ✅ Get Notifications (`replies` / `mentions` / `verified`)
  - [x] ✅ Read a user's followers list
  - [x] ✅ Read a user's following list
- [x] ✅ Read Public Data
  - [x] ✅ Read a user_id (eg. `314216`) via username(eg. `zuck`)
  - [x] ✅ Read a user's profile info
  - [x] ✅ Read list of a user's Threads
  - [x] ✅ Read list of a user's Replies
  - [x] ✅ Read Post and a list of its Replies
  - [x] ✅ View who liked a post
- [x] ✅  CI/CD
  - [x] ✅  GitHub Actions Pipeline
- [x] ✅  HTTP Clients
  - [x] ✅  AioHTTP
  - [x] ✅  Requests
  - [x] ✅  Instagrapi

## Usage Examples
View [examples/public_api_examples.py](https://github.com/Danie1/threads-api/blob/main/examples/public_api_examples.py) for Public API code examples. 

Run as:
``` bash
python3 examples/public_api_examples.py
```

View [examples/private_api_examples.py](https://github.com/Danie1/threads-api/blob/main/examples/private_api_examples.py) for Private API code examples.  (🔒 Requires Authentication 🔒)

Run as:
```
USERNAME=<Instagram Username> PASSWORD=<Instagram Password> python3 examples/private_api_examples.py
```

> **Note:**
> At the end of the file you will be able to uncomment and run the individual examples with ease.

## 📌 Roadmap
- [ ] 🚧 Share a video
- [ ] 🚧 Documentation Improvements
- [ ] 🚧 Add coverage Pytest + Coverage Widget to README


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

# License
This project is licensed under the MIT license.
