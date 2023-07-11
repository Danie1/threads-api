from typing import Optional, Dict, Union, List
import aiohttp
import re
import json
import asyncio
import json
import random
from datetime import datetime
import urllib.parse
import random
import urllib
import os
import mimetypes
import uuid
import time
import traceback
import copy

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BASE_URL = "https://i.instagram.com/api/v1"
LOGIN_URL = BASE_URL + "/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/"
POST_URL_TEXTONLY = BASE_URL + "/media/configure_text_only_post/"
POST_URL_IMAGE = BASE_URL + "/media/configure_text_post_app_feed/"
DEFAULT_HEADERS = {
            'Authority': 'www.threads.net',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.threads.net',
            'Pragma': 'no-cache',
             'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
            ),
            'X-ASBD-ID': '129477',
            'X-FB-LSD': 'NjppQDEgONsU_1LCzrmp6q',
            'X-IG-App-ID': '238260118697367',
        }

class ThreadsAPIOptions:
    def __init__(self, token: Optional[str] = None):
        self.token = token

class SimpleEncDec:
    backend = default_backend()
    iterations = 100_000

    @staticmethod
    def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=iterations, backend=SimpleEncDec.backend)
        return b64e(kdf.derive(password))

    @staticmethod
    def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
        salt = secrets.token_bytes(16)
        key = SimpleEncDec._derive_key(password.encode(), salt, iterations)
        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )

    @staticmethod
    def password_decrypt(token: bytes, password: str) -> bytes:
        decoded = b64d(token)
        salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = SimpleEncDec._derive_key(password.encode(), salt, iterations)
        return Fernet(key).decrypt(token)

class LoggedOutException(Exception):
     def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class ThreadsAPI:
    def __init__(self, options: Optional[ThreadsAPIOptions] = None):
        self.token = None
        self.user_id = None

        if options and options.token:
            self.token = options.token

        self.is_logged_in = False
        self.auth_headers = None

        self.FBLSDToken = 'NjppQDEgONsU_1LCzrmp6q'

    async def _get_public_headers(self) -> str:
        default_headers = copy.deepcopy(DEFAULT_HEADERS)
        default_headers['X-FB-LSD'] = await self._refresh_public_token()
        return default_headers
    
    async def _refresh_public_token(self) -> str:
        modified_default_headers = copy.deepcopy(DEFAULT_HEADERS)
        del modified_default_headers['X-FB-LSD']
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.instagram.com/instagram', headers=modified_default_headers) as response:
                data = await response.text()
                token_key_value = re.search('LSD",\\[\\],{"token":"(.*?)"},\\d+\\]', data).group()
                token_key_value = token_key_value.replace('LSD",[],{"token":"', '')
                token = token_key_value.split('"')[0]

        self.FBLSDToken = token
        return self.FBLSDToken
    
    async def login(self, username, password, cached_token_path=None):
        """
        Logs in the user with the provided username and password.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            bool: True if the login is successful, False otherwise.

        Raises:
            Exception: If the username or password are invalid, or if an error occurs during login.
        """
        def _save_token_to_cache(cached_token_path, token, password):
            with open(cached_token_path, "wb") as fd:
                fd.write(SimpleEncDec.password_encrypt(token.encode(), password))
            return

        def _get_token_from_cache(cached_token_path, password):
            with open(cached_token_path, "rb") as fd:
                encrypted_token = fd.read()
            return SimpleEncDec.password_decrypt(encrypted_token, password).decode()
        
        async def _set_logged_in_state(username, token):
            self.token = token
            self.user_id = await self.get_user_id_from_username(username)
            self.auth_headers = {
                'Authorization': f'Bearer IGT:2:{self.token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            self.is_logged_in = True
            return

        if username is None or password is None:
            raise Exception("Username or password are invalid")

        self.username = username

        # Look in cache before logging in.
        if cached_token_path is not None and os.path.exists(cached_token_path):
            try:
                await _set_logged_in_state(username, _get_token_from_cache(cached_token_path, password))
                
                return True
            except LoggedOutException as e:
                print(f"[Error] {e}. Attempting to re-login.")
                pass
            
        try:
            blockVersion = "5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73"
            headers = {
                "User-Agent": "Barcelona 289.0.0.77.109 Android",
                "Sec-Fetch-Site": "same-origin",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            params = json.dumps(
                {
                    "client_input_params": {
                        "password": password,
                        "contact_point": username,
                        "device_id": f"android-{random.randint(0, 1e24):x}",
                    },
                    "server_params": {
                        "credential_type": "password",
                        "device_id": f"android-{random.randint(0, 1e24):x}",
                    },
                }
            )
            bk_client_context = json.dumps(
                {"bloks_version": blockVersion, "styles_id": "instagram"}
            )

            payload = f"params={urllib.parse.quote(params)}&bk_client_context={urllib.parse.quote(bk_client_context)}&bloks_versioning_id={blockVersion}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(LOGIN_URL, timeout=60 * 1000, headers=headers, data=payload) as response:
                    data = await response.text()

            if data == "Oops, an error occurred.":
                raise Exception("Failed to login")

            pos = data.split("Bearer IGT:2:")
            if len(pos) > 1:
                pos = pos[1]
                pos = pos.split("==")[0]
                token = f"{pos}=="
                
                await _set_logged_in_state(username, token)
                
                if cached_token_path is not None:
                    _save_token_to_cache(cached_token_path, token)
                return True
            else:
                raise Exception("Error with the login response")
        except Exception as e:
            print("[ERROR] ", e)
            raise

    async def __auth_required_post_request(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.auth_headers) as response:
                return await response.json()
    
    async def __auth_required_get_request(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.auth_headers) as response:
                return await response.json()
    

    async def get_user_id_from_username(self, username: str) -> str:
        """
        Retrieves the user ID associated with a given username.
        
        Args:
            username (str): The username to retrieve the user ID for.
        
        Returns:
            str: The user ID if found, or None if the user ID is not found.
        """
        if self.is_logged_in:
            url = BASE_URL + f"/users/{username}/usernameinfo/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.auth_headers) as response:
                    data = await response.json()
                    
                    if 'message' in data and data['message'] == "login_required" or \
                        'status' in data and data['status'] == 'fail':
                        raise LoggedOutException(str(data))
                    user_id = int(data['user']['pk'])
                    return user_id
        else:
            url = f"https://www.threads.net/@{username}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=await self._get_public_headers()) as response:
                    text = await response.text()

            text = text.replace('\\s', "").replace('\\n', "")
            user_id = re.search(r'"props":{"user_id":"(\d+)"},', text)

            return user_id.group(1) if user_id else None

    async def get_user_profile(self, user_id: str):
        """
        Retrieves the profile information for a user with the provided user ID.

        Args:
            user_id (str): The user ID for which to retrieve the profile information.

        Returns:
            dict: A dictionary containing the user profile information.

        Raises:
            Exception: If an error occurs during the profile retrieval process.
        """
        url = 'https://www.threads.net/api/graphql'

        modified_headers = copy.deepcopy(await self._get_public_headers())

        modified_headers.update({
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'BarcelonaProfileRootQuery',
            'x-fb-lsd': self.FBLSDToken,
        })
        
        payload = {
                'lsd': self.FBLSDToken,
                'variables': json.dumps(
                    {
                        'userID': user_id,
                    }
                ),
                'doc_id': '23996318473300828'
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=modified_headers, data=payload) as response:
                text = await response.text()
                data = json.loads(text)
               
        user = data['data']['userData']['user']
        return user

    async def get_user_threads(self, user_id: str):
        """
        Retrieves the threads associated with a user with the provided user ID.

        Args:
            user_id (str): The user ID for which to retrieve the threads.

        Returns:
            list: A list of dictionaries representing the threads associated with the user.

        Raises:
            Exception: If an error occurs during the thread retrieval process.
        """
        url = 'https://www.threads.net/api/graphql'
        
        modified_headers = copy.deepcopy(await self._get_public_headers())

        modified_headers.update({
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'BarcelonaProfileThreadsTabQuery',
            'x-fb-lsd': self.FBLSDToken,
        })
        
        payload = {
                'lsd': self.FBLSDToken,
                'variables': json.dumps(
                    {
                        'userID': user_id,
                    }
                ),
                'doc_id': '6307072669391286'
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=modified_headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['mediaData']['threads']
        return threads
    
    async def get_user_replies(self, user_id: str):
        """
        Retrieves the replies associated with a user with the provided user ID.

        Args:
            user_id (str): The user ID for which to retrieve the replies.

        Returns:
            list: A list of dictionaries representing the replies associated with the user.

        Raises:
            Exception: If an error occurs during the thread retrieval process.
        """
        url = 'https://www.threads.net/api/graphql'

        modified_headers = copy.deepcopy(await self._get_public_headers())

        modified_headers.update({
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'BarcelonaProfileRepliesTabQuery',
            'x-fb-lsd': self.FBLSDToken,
        })
        
        payload = {
                'lsd': self.FBLSDToken,
                'variables': json.dumps(
                    {
                        'userID': user_id,
                    }
                ),
                'doc_id': '6307072669391286'
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=modified_headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['mediaData']['threads']
        return threads

    async def get_user_followers(self, user_id: str) -> bool:
        if not self.is_logged_in:
            raise Exception("The action 'get_user_followers' can only be perfomed while logged-in")
        
        res = await self.__auth_required_get_request(f"{BASE_URL}/friendships/{user_id}/followers")
        return res

    async def get_user_following(self, user_id: str) -> bool:
        if not self.is_logged_in:
            raise Exception("The action 'get_user_following' can only be perfomed while logged-in")
        
        res = await self.__auth_required_get_request(f"{BASE_URL}/friendships/{user_id}/following")
        return res

    async def follow_user(self, user_id: str) -> bool:
        """
        Follows a user with the given user ID.

        Args:
            user_id (str): The ID of the user to follow.

        Returns:
            bool: True if the user was followed successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the follow process.
        """
        if not self.is_logged_in:
            raise Exception("The action 'follow_user' can only be perfomed while logged-in")
        
        res = await self.__auth_required_post_request(f"{BASE_URL}/friendships/create/{user_id}/")
        return res["status"] == "ok"

    async def unfollow_user(self, user_id: str) -> bool:
        """
        Unfollows a user with the given user ID.

        Args:
            user_id (str): The ID of the user to unfollow.

        Returns:
            bool: True if the user was unfollowed successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the unfollow process.
        """
        if not self.is_logged_in:
            raise Exception("The action 'unfollow_user' can only be perfomed while logged-in")
        
        res = await self.__auth_required_post_request(f"{BASE_URL}/friendships/destroy/{user_id}/")
        return res["status"] == "ok"

    async def like_post(self, post_id: str) -> bool:
        """
        Likes a post with the given ID.

        Args:
            user_id (str): The ID of the post to like.

        Returns:
            bool: True if the post was liked successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the like process.
        """
        if not self.is_logged_in:
            raise Exception("The action 'like_post' can only be perfomed while logged-in")
        
        res = await self.__auth_required_post_request(f"{BASE_URL}/media/{post_id}_{self.user_id}/like/")
        return res["status"] == "ok"
    
    async def unlike_post(self, post_id: str) -> bool:
        """
        Unlikes a post with the given ID.

        Args:
            user_id (str): The ID of the post to unlike.

        Returns:
            bool: True if the post was unliked successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the like process.
        """
        if not self.is_logged_in:
            raise Exception("The action 'unlike_post' can only be perfomed while logged-in")
        
        res = await self.__auth_required_post_request(f"{BASE_URL}/media/{post_id}_{self.user_id}/unlike/")
        return res["status"] == "ok"
    
    async def delete_post(self, post_id: str) -> bool:
        """
        Deletes a post with the given ID.

        Args:
            user_id (str): The ID of the post to delete.

        Returns:
            bool: True if the post was deleted successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        if not self.is_logged_in:
            raise Exception("The action 'delete_post' can only be perfomed while logged-in")
        
        res = await self.__auth_required_post_request(f"{BASE_URL}/media/{post_id}_{self.user_id}/delete/?media_type=TEXT_POST")
        return res["status"] == "ok"
    
    async def get_post_id_from_url(self, post_url):
        """
        Retrieves the post ID from a given URL.

        Args:
            post_url (str): The URL of the post.
        Returns:
            str: The post ID if found, or None if the post ID is not found.

        Raises:
            Exception: If an error occurs during the post ID retrieval process.
        """        
        async with aiohttp.ClientSession() as session:
            async with session.get(post_url, headers=await self._get_public_headers()) as response:
                text = await response.text()

        text = text.replace('\\s', "").replace('\\n', "")
        post_id = re.search(r'"props":{"post_id":"(\d+)"},', text)
        return post_id.group(1)

    async def get_post(self, post_id: str):
        """
        Retrieves the post information for a given post ID.

        Args:
            post_id (str): The ID of the post.

        Returns:
            dict: A dictionary representing the post information.

        Raises:
            Exception: If an error occurs during the post retrieval process.
        """
        url = 'https://www.threads.net/api/graphql'
        
        modified_headers = copy.deepcopy(await self._get_public_headers())

        modified_headers.update({
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'BarcelonaPostPageQuery',
            'x-fb-lsd': self.FBLSDToken,
        })
        
        payload = {
                'lsd': self.FBLSDToken,
                'variables': json.dumps(
                    {
                        'postID': post_id,
                    }
                ),
                'doc_id': '5587632691339264',
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=modified_headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['data']
        return threads
    
    async def get_post_likes(self, post_id:int):
        """
        Retrieves the likes for a post with the given post ID.

        Args:
            post_id (int): The ID of the post.

        Returns:
            list: A list of users who liked the post.

        Raises:
            Exception: If an error occurs during the post likes retrieval process.
        """
        url = 'https://www.threads.net/api/graphql'
        
        modified_headers = copy.deepcopy(await self._get_public_headers())

        modified_headers.update({
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'BarcelonaPostPageQuery',
            'x-fb-lsd': self.FBLSDToken,
        })

        payload = {
                'lsd': self.FBLSDToken,
                'variables': json.dumps(
                    {
                        'mediaID': post_id,
                    }
                ),
                'doc_id': '9360915773983802',
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=modified_headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        return data['data']['likers']['users']

    async def post(
        self, caption: str, image_path: str = None, url: str = None, parent_post_id: str = None
    ) -> bool:
        """
        Creates a new post with the given caption, image, URL, and parent post ID.

        Args:
            caption (str): The caption of the post.
            image_path (str, optional): The path to the image file to be posted. Defaults to None.
            url (str, optional): The URL to be attached to the post. Defaults to None.
            parent_post_id (str, optional): The ID of the parent post if this post is a reply. Defaults to None.

        Returns:
            bool: True if the post was created successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the post creation process.
        """
        def __get_app_headers() -> dict:
            headers = {
                "User-Agent": f"Barcelona 289.0.0.77.109 Android",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            if self.token is not None:
                headers["Authorization"] = f"Bearer IGT:2:{self.token}"
            return headers

        async def __is_valid_url(url: str) -> bool:
            url_pattern = re.compile(
                r"^(https?://)?"
                r"((([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])\.)+[a-zA-Z]{2,})"
                r"(/?|/[-a-zA-Z0-9_%+.~!@#$^&*(){}[\]|/\\<>]*)$"
            )
            if re.match(url_pattern, url) is not None:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head(url) as response:
                            return response.status == 200
                except aiohttp.ClientError:
                    return False
            return False

        async def __download(url: str) -> bytes:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        return await response.read()
            except aiohttp.ClientError as e:
                raise Exception("[ERROR] failed to load file: ", e)

        async def __upload_image(image_url: str, image_content: bytes) -> str:
            headers = __get_app_headers().copy()

            upload_id = int(time.time() * 1000)
            name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"
            url = "https://www.instagram.com/rupload_igphoto/" + name
            mime_type = None
            if image_content is None:
                with open(image_url, mode="rb") as f:
                    content = f.read()
                mime_type, _ = mimetypes.guess_type(image_url)
            else:
                content = image_content
                async with aiohttp.ClientSession() as session:
                    async with session.head(image_url) as response:
                        content_type = response.headers.get("Content-Type")
                        if not content_type:
                            file_name = url.split("/")[-1]
                            mime_type, _ = mimetypes.guess_type(file_name)
                        if mime_type is None:
                            mime_type = "jpeg"

            x_instagram_rupload_params = {
                "upload_id": f"{upload_id}",
                "media_type": "1",
                "sticker_burnin_params": "[]",
                "image_compression": json.dumps(
                    {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
                ),
                "xsharing_user_ids": "[]",
                "retry_context": {
                    "num_step_auto_retry": "0",
                    "num_reupload": "0",
                    "num_step_manual_retry": "0",
                },
                "IG-FB-Xpost-entry-point-v2": "feed",
            }
            content_length = len(content)
            if mime_type.startswith("image/"):
                mime_type = mime_type.replace("image/", "")
            image_headers = {
                "X_FB_PHOTO_WATERFALL_ID": str(uuid.uuid4()),
                "X-Entity-Type": "image/" + mime_type,
                "Offset": "0",
                "X-Instagram-Rupload-Params": json.dumps(x_instagram_rupload_params),
                "X-Entity-Name": f"{name}",
                "X-Entity-Length": f"{content_length}",
                "Content-Type": "application/octet-stream",
                "Content-Length": f"{content_length}",
                "Accept-Encoding": "gzip",
            }

            headers.update(image_headers)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=content) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception("Failed to upload image")

        if not self.is_logged_in:
            raise Exception("You need to login before posting")
        
        now = datetime.now()
        timezone_offset = (datetime.now() - datetime.utcnow()).seconds

        params = {
            "text_post_app_info": {"reply_control": 0},
            "timezone_offset": "-" + str(timezone_offset),
            "source_type": "4",
            "_uid": self.user_id,
            "device_id": str(f"android-{random.randint(0, 1e24):x}"),
            "caption": caption,
            "upload_id": str(int(now.timestamp() * 1000)),
            "device": {
                "manufacturer": "OnePlus",
                "model": "ONEPLUS+A3010",
                "android_version": 25,
                "android_release": "7.1.1",
            },
        }
        post_url = POST_URL_TEXTONLY
        if image_path is not None:
            post_url = POST_URL_IMAGE
            image_content = None
            if not (os.path.isfile(image_path) and os.path.exists(image_path)):
                if not __is_valid_url(image_path):
                    return False
                else:
                    image_content = await __download(image_path)
            upload_id = await __upload_image(image_url=image_path, image_content=image_content)
            if upload_id is None:
                return False
            params["upload_id"] = upload_id["upload_id"]
            params["scene_capture_type"] = ""
        elif url is not None:
            params["text_post_app_info"]["link_attachment_url"] = url
        if image_path is None:
            params["publish_mode"] = "text_post"

        if parent_post_id is not None:
            params["text_post_app_info"]["reply_id"] = parent_post_id
        params = json.dumps(params)
        payload = f"signed_body=SIGNATURE.{urllib.parse.quote(params)}"
        headers = __get_app_headers().copy()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(post_url, headers=headers, data=payload) as response:
                    data = await response.json()

                    if 'media' in data and 'pk' in data['media']:
                        # Return the newly created post_id
                        return data['media']['pk']
                    else:
                        raise Exception("Failed to post. Got response:\n" + str(response))
        except Exception as e:
            print("[ERROR] ", e)
            raise