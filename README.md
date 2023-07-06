# [<img src="./.github/logo.jpg" width="36" height="36" />](https://github.com/junhoyeo) Threads API

[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)](https://www.npmjs.com/package/threads-api) [![MIT License](https://img.shields.io/badge/license-MIT-blue?style=flat-square&labelColor=black)](https://github.com/junhoyeo/threads-api/blob/main/license) [![Prettier Code Formatting](https://img.shields.io/badge/code_style-prettier-brightgreen.svg?style=flat-square&labelColor=black)](https://prettier.io)

> Unofficial, Reverse-Engineered Python client for Meta's [Threads](https://threads.net).

Inspired by [NPM Threads-API](https://github.com/junhoyeo/threads-api)

# Threads API - Python

Threads API is an unofficial Python client for Meta's Threads API. It allows you to interact with the API to retrieve user profile information, user IDs, and user profile threads.

# Usage
### "get_user_id_from_username" Function
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

### "get_user_profile_threads" Function
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

### "get_user_profile_threads" Function
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

## 📦 Installation

```bash
poetry install threads-api
```

```typescript
// or in Deno 🦖
import { ThreadsAPI } from "npm:threads-api";

## 📌 Roadmap

- [x] ✅ Read public data\
  - [x] ✅ Fetch UserID(`314216`) via username(`zuck`)
  - [x] ✅ Read user profile info
  - [x] ✅ Read list of user Threads
  - [ ] 🚧 Read list of user replies
  - [ ] 🚧 Read single Thread
- [ ] 🚧 Read private data
- [ ] 🚧 Write data (i.e. write automated Threads)
- [ ]🚧  CI/CD
  - [ ]🚧  Pytest
  - [ ]🚧  GitHub Actions Pipeline


# License
This project is licensed under the MIT license.