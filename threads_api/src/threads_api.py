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
import copy

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import logging
import sys
from threads_api.src.anotherlogger import format_log
from threads_api.src.anotherlogger import log_debug
from colorama import init, Fore, Style
import functools
from threads_api.src.settings import Settings

from threads_api.src.http_sessions.aiohttp_session import AioHTTPSession
from threads_api.src.types import *

OPEN_ISSUE_MESSAGE = f"{Fore.RED}Oops, this is an error that hasn't yet been properly handled.\nPlease open an issue on Github at https://github.com/Danie1/threads-api.{Style.RESET_ALL}"

BASE_URL = "https://i.instagram.com/api/v1"
LOGIN_URL = BASE_URL + "/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/"
POST_URL_TEXTONLY = BASE_URL + "/media/configure_text_only_post/"
POST_URL_IMAGE = BASE_URL + "/media/configure_text_post_app_feed/"
POST_URL_SIDECAR = BASE_URL + "/media/configure_text_post_app_sidecar/"
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

def require_login(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.is_logged_in:
            raise Exception(f"The action '{func.__name__}' can only be perfomed while logged-in")
        return await func(self, *args, **kwargs)
    return wrapper

class ThreadsAPI:
    def __init__(self, http_session_class=AioHTTPSession, settings_path : str=".session.json"):

        # Get the log level from the environment variable
        log_level_env = os.environ.get("LOG_LEVEL", "WARNING")

        # Set the log level based on the environment variable
        log_level = getattr(logging, log_level_env.upper(), None)
        if not isinstance(log_level, int):
            raise ValueError(f"Invalid log level: {log_level_env}")
        
        self.log_level = log_level
        
        self.set_log_level(self.log_level)

        self.logger = logging.getLogger(name="ThreadsAPILogger")
        

        # Setup settings
        self.settings_path = settings_path
        self.settings = Settings()

        # Check if settings_path is configured
        if settings_path is not None:
            if os.path.exists(settings_path):
                self.settings.load_settings(settings_path)
            else:
                # Create settings file on filesystem if it doesn't exist already
                self.settings.dump_settings(settings_path)
        
        # Set the HTTP client class to use when initializing sessions
        self.http_session_class = http_session_class

        # Setup public connection members
        self._public_session = self.http_session_class()

        # Setup private connection members
        self._auth_session = self.http_session_class()
        self.token = None
        self.user_id = None
        self.is_logged_in = False
        self.auth_headers = None

        self.FBLSDToken = 'NjppQDEgONsU_1LCzrmp6q'

        # Log all configureable attributes for troubleshooting
        self.logger.info(format_log(message="ThreadsAPI.__init__ Configurations",
            settings_path=self.settings_path,
            log_level=self.log_level,
            http_session_class=self.http_session_class.__name__,
            settings=self.settings.get_settings()))

    def set_log_level(self, log_level):
        self.log_level = log_level
        logging.basicConfig(level=self.log_level, format='%(levelname)s:%(message)s')

    def _extract_response_json(self, response):
        try:
            resp = json.loads(response)            
        except (aiohttp.ContentTypeError, json.JSONDecodeError):
            if response.find("not-logged-in") > 0:
                raise Exception(f"You're trying to perform an operation without permission. Check: Are you logged into the correct user? Can you perform the action on the input provided?")
            else:
                raise Exception(f'Failed to decode response [{response}] as JSON.\n\n{OPEN_ISSUE_MESSAGE}')

        return resp

    @require_login
    async def _private_post(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='POST', **kwargs)
        response = await self._auth_session.post(**kwargs)
        resp_json = self._extract_response_json(response)
        log_debug(title='PRIVATE RESPONSE', response=resp_json)
        
        if 'status' in resp_json and resp_json['status'] == 'fail' or \
            'errors' in resp_json:
            raise Exception(f"Request Failed, got back: [{resp_json}]\n{OPEN_ISSUE_MESSAGE}")
    
        return resp_json
    

    @require_login
    async def _private_get(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='GET', **kwargs)
        response = await self._auth_session.get(**kwargs)
        resp_json = self._extract_response_json(response)
        log_debug(title='PRIVATE RESPONSE', response=resp_json)
        
        if 'status' in resp_json and resp_json['status'] == 'fail' or \
            'errors' in resp_json:
            if 'message' in resp_json and resp_json['message'] == 'challenge_required':
                raise LoggedOutException("It appears you have been logged out.")
            raise Exception(f"Request Failed, got back: [{resp_json}]\n{OPEN_ISSUE_MESSAGE}")
    
        return resp_json
    

    async def _public_post_json(self, **kwargs):
        log_debug(title='PUBLIC REQUEST', type='POST', **kwargs)
        response = await self._public_session.post(**kwargs)
        resp_json = self._extract_response_json(response)
        log_debug(title='PUBLIC RESPONSE', response=resp_json)
        
        if 'status' in resp_json and resp_json['status'] == 'fail' or \
            'errors' in resp_json:
            raise Exception(f"Request Failed, got back: [{resp_json}]\n{OPEN_ISSUE_MESSAGE}")
    
        return resp_json
    
    async def _public_get_json(self, **kwargs):
        log_debug(title='PUBLIC REQUEST', type='GET', **kwargs)
        response = await self._public_session.get(**kwargs)
        resp_json = self._extract_response_json(response)
        log_debug(title='PUBLIC RESPONSE', response=resp_json)
        
        if 'status' in resp_json and resp_json['status'] == 'fail' or \
            'errors' in resp_json:
            raise Exception(f"Request Failed, got back: [{resp_json}]\n{OPEN_ISSUE_MESSAGE}")
    
        return resp_json
    
    async def _public_post_text(self, **kwargs):
        log_debug(title='PUBLIC REQUEST', type='POST', **kwargs)
        response = await self._public_session.post(**kwargs)
        log_debug(title='PUBLIC RESPONSE', response=response)
        
        return response

    async def _public_get_text(self, **kwargs):
        log_debug(title='PUBLIC REQUEST', type='GET', **kwargs)
        response = await self._public_session.get(**kwargs)
        log_debug(title='PUBLIC RESPONSE', response=response)

        return response

    async def load_settings(self, path: str = None):
        return self.settings.load_settings(path)
    
    async def dump_settings(self, path: str = None):
        return self.settings.dump_settings(path)

    async def _get_public_headers(self) -> str:
        default_headers = copy.deepcopy(DEFAULT_HEADERS)
        default_headers['X-FB-LSD'] = await self._refresh_public_token()
        return default_headers
    
    async def _refresh_public_token(self) -> str:
        self.logger.info("Refreshing public token")
        modified_default_headers = copy.deepcopy(DEFAULT_HEADERS)
        del modified_default_headers['X-FB-LSD']
        url = 'https://www.instagram.com/instagram'

        data = await self._public_get_text(url=url, headers=modified_default_headers)

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
                encrypted_token = SimpleEncDec.password_encrypt(token.encode(), password)
                fd.write(encrypted_token)
                self.logger.info("Saved token encrypted to cache")

                # Sync token between original token cache and the settings file
                self.settings.set_encrypted_token(encrypted_token.decode())

                if self.settings_path is not None:
                    self.settings.dump_settings(self.settings_path)
                    self.logger.info("Saved token encrypted to settings file")
            return

        def _get_token_from_cache(cached_token_path, password):
            decrypted_token = None

            # Try to load the token from the settings file before looking in the original token cache
            if self.settings_path is not None:
                try:
                    self.settings.load_settings(self.settings_path)
                    
                    if self.settings.encrypted_token is not None:
                        decrypted_token = SimpleEncDec.password_decrypt(self.settings.encrypted_token.encode(), password).decode()
                        self.logger.info("Loaded encrypted token from settings file")
                except FileNotFoundError:
                    # Use default settings if the file does not exist yet
                    self.logger.info(f"Using default settings because no file was found in {self.settings_path}")
                    pass

            # stop using cached_token_path if encrypted_token exists in settings file
            if decrypted_token is None:
                with open(cached_token_path, "rb") as fd:
                    encrypted_token = fd.read()
                    
                    # Sync token between original token cache and the settings file
                    self.settings.set_encrypted_token(encrypted_token.decode())
                    self.settings.dump_settings(self.settings_path)

                    decrypted_token = SimpleEncDec.password_decrypt(encrypted_token, password).decode()
                    self.logger.info("Loaded encrypted token from cache")
            return decrypted_token
        
        async def _set_logged_in_state(username, token):
            self.token = token
            self.auth_headers = {
                'Authorization': f'Bearer IGT:2:{self.token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
            self.is_logged_in = True
            self.user_id = await self.get_user_id_from_username(username)
            self.logger.info("Set logged-in state successfully. All set!")
            return
        
        if username is None or password is None:
            raise Exception("Username or password are invalid")

        self.username = username

        # Look in cache before logging in.
        if cached_token_path is not None and os.path.exists(cached_token_path):
            self.logger.info(f"Found cache file in {cached_token_path}, attempting to read the token from it.")
            try:
                await _set_logged_in_state(username, _get_token_from_cache(cached_token_path, password))
                return True
            except LoggedOutException as e:
                print(f"[Error] {e}. Attempting to re-login.")
                pass
        
        try:
            self.logger.info("Attempting to login")
            token = self._auth_session.auth(username=username, password=password)
            
            await _set_logged_in_state(username, token)
                    
            if cached_token_path is not None:
                _save_token_to_cache(cached_token_path, token, password)
        except Exception as e:
            print("[ERROR] ", e)
            raise

        return True

    async def close_gracefully(self):
        if self._auth_session is not None:
            await self._auth_session.close()
            self._auth_session = None

        if self._public_session is not None:
            await self._public_session.close()
            self._public_session = None

        self.user_id = None
        self.is_logged_in = False
        self.token = None

    async def get_user_id_from_username(self, username: str) -> str:
        """
        Retrieves the user ID associated with a given username.
        
        Args:
            username (str): The username to retrieve the user ID for.
        
        Returns:
            str: The user ID if found, or None if the user ID is not found.
        """
        if self.is_logged_in and self.username == username:
            self.logger.info(f"Fetching user_id for user [{username}] while logged-in")
            
            data = await self._private_get(url=f"{BASE_URL}/users/{username}/usernameinfo/", headers=self.auth_headers)
            
            if 'message' in data and data['message'] == "login_required" or \
                'status' in data and data['status'] == 'fail':
                if 'User not onboarded' in data['message']:
                    raise Exception(f"User {username} is not onboarded to threads.net")
                elif 'challenge_required' in data['message'] and \
                    'challenge' in data and 'url' in data['challenge'] and \
                    'https://www.instagram.com/accounts/suspended/' in data['challenge']['url']:
                    raise Exception(f"User {username} is suspended from threads.net :(")
                
                # Cross fingers you reach this exception and not the previous ones
                raise LoggedOutException(str(data))
            
            user_id = int(data['user']['pk'])
            return user_id
        else:
            self.logger.info(f"Fetching user_id for user [{username}] anonymously")
            
            headers = await self._get_public_headers()
            text = await self._public_get_text(url=f"https://www.threads.net/@{username}", headers=headers)

            text = text.replace('\\s', "").replace('\\n', "")
            user_id = re.search(r'"props":{"user_id":"(\d+)"},', text)

            return user_id.group(1) if user_id else None

    async def get_user_profile(self, user_id: str) -> User:
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
    
        data = await self._public_post_json(url=url, headers=modified_headers, data=payload)

        return User(**data['data']['userData']['user'])

    async def get_user_threads(self, user_id: str, count=10, max_id=None) -> Threads:
        """
        Retrieves the threads associated with a user with the provided user ID.

        Args:
            user_id (str): The user ID for which to retrieve the threads.

        Returns:
            list: A list of dictionaries representing the threads associated with the user.

        Raises:
            Exception: If an error occurs during the thread retrieval process.
        """
        if self.is_logged_in:
            if max_id is not None:
                params = {'count': count, 'max_id':max_id}
            else:
                params = {'count': count}
            resp = await self._private_get(url=f'{BASE_URL}/text_feed/{user_id}/profile/', headers=self.auth_headers,data=params)

            return Threads(**resp)
        # Public API for getting user threads is minimal. 'count' and 'max_id' are not used.
        else:
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
                    'doc_id': '6232751443445612'
                }
            
            data = await self._public_post_json(url=url, headers=modified_headers, data=payload)
            
            threads = Threads(**data['data']['mediaData'])
            return threads
    
    async def get_user_replies(self, user_id: str, count=10, max_id : str = None) -> Threads:
        """
        Retrieves the replies associated with a user with the provided user ID.

        Args:
            user_id (str): The user ID for which to retrieve the replies.

        Returns:
            list: A list of dictionaries representing the replies associated with the user.

        Raises:
            Exception: If an error occurs during the thread retrieval process.
        """
        if self.is_logged_in:
            if max_id is not None:
                params = {'count': count, 'max_id':max_id}
            else:
                params = {'count': count}
            resp = await self._private_get(url=f'{BASE_URL}/text_feed/{user_id}/profile/replies', headers=self.auth_headers,data=params)

            return Threads(**resp)
        # Public API for getting user threads is minimal. 'count' and 'max_id' are not used.
        else:
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

            data = await self._public_post_json(url=url, headers=modified_headers, data=payload)

            threads = Threads(**data['data']['mediaData'])
            return threads
    
    async def get_post_id_from_url(self, post_url : str):
        """
        Retrieves the post ID from a given URL.

        Args:
            post_url (str): The URL of the post.
        Returns:
            str: The post ID if found, or None if the post ID is not found.

        Raises:
            Exception: If an error occurs during the post ID retrieval process.
        """        
        if "https://" in post_url and "/@" in post_url:
            raise Exception(f"Argument {post_url} is not a valid URL")
        elif "https://" in post_url and "/t" in post_url:
            shortcode = post_url.split("/t/")[-1].split("/")[0]
        elif len(post_url) == 11:
            shortcode = post_url
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        id = 0
        for char in shortcode:
            id = (id * 64) + alphabet.index(char)
        return str(id)

    async def get_post(self, post_id: str, count=10, max_id=None) -> Replies:
        """
        Retrieves the post information for a given post ID.

        Args:
            post_id (str): The ID of the post.

        Returns:
            dict: A dictionary representing the post information.

        Raises:
            Exception: If an error occurs during the post retrieval process.
        """
        
        if self.is_logged_in:
            if max_id is not None:
                params = {'count': count, 'max_id':max_id}
            else:
                params = {'count': count}
            data = await self._private_get(url=f'{BASE_URL}/text_feed/{post_id}/replies', headers=self.auth_headers, data=params)
            response = Replies(**data)
        else:
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

            data = await self._public_post_json(url=url, headers=modified_headers, data=payload)

            response = Replies(**data['data']['data'])
        return response
    
    async def get_post_likes(self, post_id:str) -> UsersList:
        """
        Retrieves the likes for a post with the given post ID.

        Args:
            post_id (str): The ID of the post.

        Returns:
            list: A list of users who liked the post.

        Raises:
            Exception: If an error occurs during the post likes retrieval process.
        """
        if self.is_logged_in:
            data = await self._private_get(url=f'{BASE_URL}/media/{post_id}_{self.user_id}/likers', headers=self.auth_headers)
            response = UsersList(**data)
        else:
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

            data = await self._public_post_json(url=url, headers=modified_headers, data=payload)

            response = UsersList(**data['data']['likers'])
        return response

    @require_login
    async def repost(self, post_id : str):
        """
        Repost a post.

        Args:
            post_id (int): a post's identifier.

        Returns:
            The reposting information as a dict.
        """
        return await self._private_post(url=f'{BASE_URL}/repost/create_repost/', headers=self.auth_headers, data=f'media_id={post_id}')

    @require_login
    async def delete_repost(self, post_id:str):
        """
        Delete a repost.

        Args:
            post_id (int): a post's identifier.

        Returns:
            The unreposting information as a dict.
        """
        return await self._private_post(url=f'{BASE_URL}/repost/delete_text_app_repost/', headers=self.auth_headers, data=f'original_media_id={post_id}')

    @require_login
    async def get_user_followers(self, user_id: str) -> bool:
        res = await self._private_post(f"{BASE_URL}/friendships/{user_id}/followers", headers=self.auth_headers)
        return res

    @require_login
    async def get_user_following(self, user_id: str) -> bool:
        res = await self._private_post(f"{BASE_URL}/friendships/{user_id}/following", headers=self.auth_headers)
        return res

    @require_login
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
        res = await self._private_post(url=f"{BASE_URL}/friendships/create/{user_id}/", headers=self.auth_headers)
        return res["status"] == "ok"

    @require_login
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
        res = await self._private_post(url=f"{BASE_URL}/friendships/destroy/{user_id}/", headers=self.auth_headers)
        return res["status"] == "ok"

    @require_login
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
        res = await self._private_post(url=f"{BASE_URL}/media/{post_id}_{self.user_id}/like/", headers=self.auth_headers)
        return res["status"] == "ok"
    
    @require_login
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
        res = await self._private_post(url=f"{BASE_URL}/media/{post_id}_{self.user_id}/unlike/", headers=self.auth_headers)
        return res["status"] == "ok"
    
    @require_login
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
        res = await self._private_post(url=f"{BASE_URL}/media/{post_id}_{self.user_id}/delete/?media_type=TEXT_POST", headers=self.auth_headers)
        return res["status"] == "ok"
    
    @require_login
    async def get_timeline(self, maxID : str = None):
        """
        Get timeline for the authenticated user

        Args:
            maxID (int): The ID token for the next batch of posts

        Returns:
            list: REST API JSON data response for the get_timeline request

        Raises:
            Exception: If an error occurs during the timeline retrieval process.
        """
        # Check if you have the ID of the next batch to fetch
        if maxID is None:
            parameters = {
                    'pagination_source': 'text_post_feed_threads',
            }
        else:
            parameters = {
                    'pagination_source': 'text_post_feed_threads',
                    'max_id': maxID
            }

        res = await self._private_post(url=f'{BASE_URL}/feed/text_post_app_timeline/', headers=self.auth_headers,data=parameters)
        return TimelineData(**res)

    @require_login
    async def mute_user(self, user_id : str):
        """
        Mute a user

        Args:
            user_id (int): The ID of the user to mute.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the muting process.
        """
        parameters = json.dumps(
            obj={
                'target_posts_author_id': user_id,
                'container_module': 'ig_text_feed_timeline',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'

        res = await self._private_post(url=f'{BASE_URL}/friendships/mute_posts_or_story_from_follow/', headers=self.auth_headers, data=payload)
        return res

    @require_login
    async def unmute_user(self, user_id : str):
        """
        Unmute a user

        Args:
            user_id (int): The ID of the user to unmute.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the unmuting process.
        """
        parameters = json.dumps(
            obj={
                'target_posts_author_id': user_id,
                'container_module': 'ig_text_feed_timeline',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'

        res = await self._private_post(url=f'{BASE_URL}/friendships/unmute_posts_or_story_from_follow/', headers=self.auth_headers, data=payload)
        return res
    
    @require_login
    async def restrict_user(self, user_id : str):
        """
        Restrict a user

        Args:
            user_id (int): The ID of the user to restrict.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the restricting process.
        """
        parameters = json.dumps(
            obj={
                'user_ids': user_id,
                'container_module': 'ig_text_feed_timeline',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'

        res = await self._private_post(url=f'{BASE_URL}/restrict_action/restrict_many/', headers=self.auth_headers, data=payload)
        return res
    
    @require_login
    async def unrestrict_user(self, user_id : str):
        """
        Unrestrict a user

        Args:
            user_id (int): The ID of the user to unrestrict.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the unrestricting process.
        """
        parameters = json.dumps(
            obj={
                'user_ids': user_id,
                'container_module': 'ig_text_feed_timeline',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'
        res = await self._private_post(url=f'{BASE_URL}/restrict_action/unrestrict/', headers=self.auth_headers, data=payload)
        return res
    
    @require_login
    async def block_user(self, user_id : str):
        """
        Block a user

        Args:
            user_id (int): The ID of the user to block.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the blocking process.
        """
        parameters = json.dumps(
            obj={
                'user_id': user_id,
                'surface': 'ig_text_feed_timeline',
                'is_auto_block_enabled': 'true',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'
        res = await self._private_post(url=f'{BASE_URL}/friendships/block/{user_id}/', headers=self.auth_headers, data=payload)
        return res
    
    @require_login
    async def unblock_user(self, user_id : str):
        """
        Unblock a user

        Args:
            user_id (int): The ID of the user to unblock.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the unblocking process.
        """
        parameters = json.dumps(
            obj={
                'user_id': user_id,
                'container_module': 'ig_text_feed_timeline',
            },
        )

        encoded_parameters = urllib.parse.quote(string=parameters, safe="!~*'()")
        payload = f'signed_body=SIGNATURE.{encoded_parameters}'
        res = await self._private_post(url=f'{BASE_URL}/friendships/unblock/{user_id}/', headers=self.auth_headers, data=payload)
        return res
    
    @require_login
    async def search_user(self, query : str):
        """
        Search for a user

        Args:
            query (str): search query

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the search process.
        """
        res = await self._private_get(url=f'{BASE_URL}/users/search/?q={query}', headers=self.auth_headers)
        return res
    
    @require_login
    async def get_recommended_users(self, max_id : str = None):
        """
        Get list of recommended users

        Args:
        max_id (str) : the next page of recommended users
        #TODO This argument may not work. Still looking into this. Please open a Github Issue if you found a solution.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the search process.
        """
        max_id = f"?max_id={max_id}" if max_id else ""
        res = await self._private_get(url=f'{BASE_URL}/text_feed/recommended_users/{max_id}', headers=self.auth_headers)
        return res
    
    @require_login
    async def get_notifications(self, selected_filter : str ="text_post_app_replies", max_id : str = None, pagination_first_record_timestamp:str = None):
        """
        Get list of recommended users

        Args:
        selected_filter (str): Choose one: "text_post_app_mentions", "text_post_app_replies", "verified"

        max_id (str) : the next page of get notifications
        #TODO This argument may not work. Still looking into this. Please open a Github Issue if you found a solution.

        pagination_first_record_timestamp (str) : Timestamp of the first record for pagination
        #TODO This argument may not work. Still looking into this. Please open a Github Issue if you found a solution.

        Returns:
            dict: REST API Response in JSON format

        Raises:
            Exception: If an error occurs during the search process.
        """
        params = {'feed_type' : 'all',
                  'mark_as_seen' : False,
                  'timezone_offset':str(self.settings.timezone_offset)
        }

        if selected_filter:
            params.update({'selected_filter': selected_filter})
        
        if max_id:
            params.update({'max_id': max_id, 'pagination_first_record_timestamp': pagination_first_record_timestamp})
        
        res = await self._private_get(url=f'{BASE_URL}/text_feed/text_app_notifications/', headers=self.auth_headers, data=params)
        return res
    
    @require_login
    async def post(
        self, caption: str, image_path = None, url: str = None, parent_post_id: str = None, quoted_post_id: str = None) -> PostResponse:
        """
        Creates a new post with the given caption, image, URL, and parent post ID.

        Args:
            caption (str): The caption of the post.
            image_path (str or list, optional: The path to the image file to be posted or list of images paths. Defaults to None.
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

        def generate_next_upload_id():
            return int(time.time() * 1000)

        async def _upload_image(path: str) -> dict:
            random_number = random.randint(1000000000, 9999999999)
            upload_id = generate_next_upload_id()
            upload_name = f'{upload_id}_0_{random_number}'

            file_data = None
            file_length = None
            mime_type = 'image/jpeg'
            waterfall_id = str(uuid.uuid4())

            is_url = path.startswith('http')
            is_file_path = not path.startswith('http')

            if is_file_path:
                with open(path, 'rb') as file:
                    file_data = file.read()
                    file_length = len(file_data)

            mime_type = mimetypes.guess_type(path)[0]

            if is_url:
                response = await self._public_session.download(url=path)

                file_data = response
                file_length = len(response)

            if not is_file_path and not is_url:
                raise ValueError('Provided image URL neither HTTP(S) URL nor file path. Please, create GitHub issue')

            if file_data is None and file_length is None:
                raise ValueError('Provided image could not be uploaded. Please, create GitHub issue')

            parameters_as_string = {
                'media_type': 1,
                'upload_id': str(upload_id),
                'sticker_burnin_params': json.dumps([]),
                'image_compression': json.dumps(
                    {
                        'lib_name': 'moz',
                        'lib_version': '3.1.m',
                        'quality': '80',
                    },
                ),
                'xsharing_user_ids': json.dumps([]),
                'retry_context': json.dumps(
                    {
                        'num_step_auto_retry': '0',
                        'num_reupload': '0',
                        'num_step_manual_retry': '0',
                    },
                ),
                'IG-FB-Xpost-entry-point-v2': 'feed',
            }

            headers = self.auth_headers | {
                'Accept-Encoding': 'gzip',
                'X-Instagram-Rupload-Params': json.dumps(parameters_as_string),
                'X_FB_PHOTO_WATERFALL_ID': waterfall_id,
                'X-Entity-Type': mime_type,
                'Offset': '0',
                'X-Entity-Name': upload_name,
                'X-Entity-Length': str(file_length),
                'Content-Type': 'application/octet-stream',
                'Content-Length': str(file_length),
            }

            response = await self._private_post(url="https://www.instagram.com/rupload_igphoto/" + upload_name, headers=headers,data=file_data)
            
            if response['status'] == 'ok':
                return response
            else:
                raise Exception("Failed to upload image")
        
        now = datetime.now()
        
        params = {
            "text_post_app_info": {"reply_control": 0},
            "timezone_offset": str(self.settings.timezone_offset),
            "source_type": "4",
            "_uid": self.user_id,
            "device_id": self.settings.device_id,
            "caption": caption,
            "upload_id": str(int(now.timestamp() * 1000)),
            "device": self.settings.device_as_dict,
        }

        post_url = POST_URL_TEXTONLY
        if image_path is not None and url is None:
            if isinstance(image_path, list):
                if len(image_path) < 2:
                    raise Exception("Error: You must specify at least 2 image paths in `image_path` argument")

            if isinstance(image_path, str):
                post_url = POST_URL_IMAGE           
                upload_id = await _upload_image(path=image_path)
                if upload_id is None:
                    return False
                params["upload_id"] = upload_id["upload_id"]
                params["scene_capture_type"] = ""
            elif isinstance(image_path, list):
                post_url = POST_URL_SIDECAR
                params['client_sidecar_id'] = generate_next_upload_id()
                params["children_metadata"] = []
                for image in image_path:
                    upload_id = await _upload_image(path=image)
                    params["children_metadata"] += [{
                        'upload_id': upload_id["upload_id"],
                        'source_type': '4',
                        'timezone_offset': str(self.settings.timezone_offset),
                        'scene_capture_type': "",
                    }]
            else:
                raise Exception(f"The image_path [{image_path}] is invalid.\n{OPEN_ISSUE_MESSAGE}")
        elif url is not None:
            params["text_post_app_info"]["link_attachment_url"] = url
        
        if image_path is None:
            params["publish_mode"] = "text_post"

        if parent_post_id is not None:
            params["text_post_app_info"]["reply_id"] = parent_post_id

        if quoted_post_id is not None:
            params["text_post_app_info"]["quoted_post_id"] = quoted_post_id

        params = json.dumps(params)
        payload = f"signed_body=SIGNATURE.{urllib.parse.quote(params)}"
        headers = __get_app_headers().copy()

        try:
            res = await self._private_post(url=post_url, headers=headers,data=payload)

            if 'status' in res and res['status'] == "ok":
                return PostResponse(**res)
            else:
                raise Exception("Failed to post. Got response:\n" + str(res))
        except Exception as e:
            print("[ERROR] ", e)
            raise
