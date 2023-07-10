import requests
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

class ThreadsAPIOptions:
    def __init__(self, fbLSDToken: Optional[str] = None, 
                       token: Optional[str] = None):
        self.fbLSDToken = fbLSDToken
        self.token = token

class ThreadsAPI:
    def __init__(self, options: Optional[ThreadsAPIOptions] = None):
        self.fbLSDToken = 'NjppQDEgONsU_1LCzrmp6q'
        self.token = None
        self.user_id = None

        if options and options.fbLSDToken:
            self.fbLSDToken = options.fbLSDToken

        if options and options.token:
            self.token = options.token

    async def login(self, username, password):
        if username is None or password is None:
            raise Exception("Username or password are invalid")

        self.username = username

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

            LOGIN_URL = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/"
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
                self.token = token

                self.user_id = await self.get_user_id_from_username(username)
                return True
            else:
                raise Exception("Error with the login response")
        except Exception as e:
            print("[ERROR] ", e)
            raise

    async def get_user_id_from_username(self, username: str) -> str:
        url = f"https://www.threads.net/@{username}"
        headers = {
            "authority": "www.threads.net",
            "accept": "*/*",
            "accept-language": "ko",
            "cache-control": "no-cache",
            "origin": "https://www.threads.net",
            "pragma": "no-cache",
            "referer": f"https://www.threads.net/@{username}",
            "x-asbd-id": "129477",
            "x-fb-lsd": self.fbLSDToken,
            "x-ig-app-id": "238260118697367",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()

        text = text.replace('\\s', "").replace('\\n', "")
        user_id = re.search(r'"props":{"user_id":"(\d+)"},', text)

        lsd_token_match = re.search('"LSD",\[\],{"token":"(\w+)"},\d+\]', text)
        lsd_token = lsd_token_match.group(1) if lsd_token_match else None
        self.fbLSDToken = lsd_token

        return user_id.group(1) if user_id else None

    async def get_user_profile(self, username: str, user_id: str):
        url = 'https://www.threads.net/api/graphql'
        headers = {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.net',
            'referer': f'https://www.threads.net/@{username}',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '897',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'BarcelonaProfileRootQuery',
            'x-fb-lsd': 'I5silyPfeZJQAyrhqVdqGB',
            'x-ig-app-id': '238260118697367'
        }
        payload = {
            'av': '0',
            '__user': '0',
            '__a': '1',
            '__req': '1',
            '__hs': '19544.HYP:barcelona_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1007798382',
            '__s': 'hue11s:dyq74i:1fwaxg',
            '__hsi': '7252829167888753415',
            '__dyn': '7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE465o-cw5Mx62G3i0Bo7O2l0Fwqo31wnEfovwRwlE-U2zxe2Gew9O22362W2K0zK5o4q0GpovU1aUbodEGdwtU2ewbS1LwTwNwLw8O1pwr82gxC',
            '__csr': 'gyhelk8iS00lnm4oioC2385um28MWawVwt40km2Ordg-cGu3C4E6-2QfoJ4m8g80x6wbC0E41Jy30sQ13g0E06V08M42eNE8k0wg88gzBe',
            '__comet_req': '29',
            'lsd': 'I5silyPfeZJQAyrhqVdqGB',
            'jazoest': '22056',
            '__spin_r': '1007798382',
            '__spin_b': 'trunk',
            '__spin_t': '1688680883',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaProfileRootQuery',
            'variables': f'{{"userID":"{user_id}"}}',
            'server_timestamps': 'true',
            'doc_id': '23996318473300828'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                text = await response.text()
                data = json.loads(text)
               
        user = data['data']['userData']['user']
        return user

    async def get_user_profile_threads(self, username: str, user_id: str):
        url = 'https://www.threads.net/api/graphql'
        headers = {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.net',
            'referer': f'https://www.threads.net/@{username}',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '897',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'BarcelonaProfileThreadsTabQuery',
            'x-fb-lsd': 'I5silyPfeZJQAyrhqVdqGB',
            'x-ig-app-id': '238260118697367'
        }
        payload = {
            'av': '0',
            '__user': '0',
            '__a': '1',
            '__req': '2',
            '__hs': '19544.HYP:barcelona_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1007798382',
            '__s': 'hue11s:dyq74i:1fwaxg',
            '__hsi': '7252829167888753415',
            '__dyn': '7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE465o-cw5Mx62G3i0Bo7O2l0Fwqo31wnEfovwRwlE-U2zxe2Gew9O22362W2K0zK5o4q0GpovU1aUbodEGdwtU2ewbS1LwTwNwLw8O1pwr82gxC',
            '__csr': 'gyhelk8iS00lnm4oioC2385um28MWawVwt40km2Ordg-cGu3C4E6-2QfoJ4m8g80x6wbC0E41Jy30sQ13g0E06V08M42eNE8k0wg88gzBe',
            '__comet_req': '29',
            'lsd': 'I5silyPfeZJQAyrhqVdqGB',
            'jazoest': '22056',
            '__spin_r': '1007798382',
            '__spin_b': 'trunk',
            '__spin_t': '1688680883',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaProfileThreadsTabQuery',
            'variables': f'{{"userID":"{user_id}"}}',
            'server_timestamps': 'true',
            'doc_id': '6232751443445612'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['mediaData']['threads']
        return threads
    
    async def get_user_profile_replies(self, username: str, user_id: str):
        url = 'https://www.threads.net/api/graphql'
        headers = {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.net',
            'referer': 'https://www.threads.net/@zuck/replies',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-ch-ua-platform-version': '15.0.0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '897',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'BarcelonaProfileRepliesTabQuery',
            'x-fb-lsd': 'tu2kTRKO1aZl9rMKmRuq9u',
            'x-ig-app-id': '238260118697367',
        }
        payload = {
            'av': '0',
            '__user': '0',
            '__a': '1',
            '__req': '2',
            '__hs': '19545.HYP:barcelona_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1007803729',
            '__s': 'vg5z1u:dyq74i:zgf5h2',
            '__hsi': '7253172656040290354',
            '__dyn': '7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE465o-cw5Mx62G3i0Bo7O2l0Fwqo31wnEfovwRwlE-U2zxe2Gew9O22362W2K0zK5o4q0GpovU1aUbodEGdwtU2ewbS1LwTwNwLw8O1pwr82gxC',
            '__csr': 'gA-AlUx9k00lp25u17xS6UvwhUO3gMym8g4Ry82GwwAN0rx11dxW4E4-261wwI7Nw4i0g11l0MgeoJS1KF0Y3MV4m0aj0g8X6G7wt4a0wo-eEU',
            '__comet_req': '29',
            'lsd': 'tu2kTRKO1aZl9rMKmRuq9u',
            'jazoest': '21972',
            '__spin_r': '1007803729',
            '__spin_b': 'trunk',
            '__spin_t': '1688760858',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaProfileRepliesTabQuery',
            'variables': '{"userID":"314216"}',
            'server_timestamps': 'true',
            'doc_id': '6307072669391286',
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['mediaData']['threads']
        return threads
    
    async def get_post_id_from_url(self, post_url, options=None):
        url = post_url
        headers = {
            "authority": "www.threads.net",
            "accept": "*/*",
            "accept-language": "ko",
            "cache-control": "no-cache",
            "origin": "https://www.threads.net",
            "pragma": "no-cache",
            "referer": post_url,
            "x-asbd-id": "129477",
            "x-fb-lsd": self.fbLSDToken,
            "x-ig-app-id": "238260118697367",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()

        text = text.replace('\\s', "").replace('\\n', "")
        post_id = re.search(r'"props":{"post_id":"(\d+)"},', text)
        return post_id.group(1)

    async def get_post(self, thread_id: str):
        url = 'https://www.threads.net/api/graphql'
        headers = {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.net',
            'referer': f'https://www.threads.net/t/{thread_id}',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '897',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'BarcelonaPostPageQuery',
            'x-fb-lsd': 'bUryVn_O9_i_D9F7WOqEpA',
            'x-ig-app-id': '238260118697367',
        }

        payload = {
        'av': '0',
        '__user': '0',
        '__a': '1',
        '__req': '1',
        '__hs': '19545.HYP:barcelona_web_pkg.2.1..0.0',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1007805316',
        '__s': 'tygnis:dyq74i:zuyk3e',
        '__hsi': '7253177132820350526',
        '__dyn': '7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE5ufz81s8hwGwQw9m1YwBgao6C0Mo5W3S7Udo5qfK0EUjwGzE2swwwNwKwHw8Xxm16waCm7-0iK2S3qazo7u0zE2ZwrUdUcobU2cwmo6O0A8pw',
        '__csr': 'hI_yaUBb9sE01kRm1syToiwHc0sW1czEgDc11wwG0Qk1Hw1Co40tixLOw',
        '__comet_req': '29',
        'lsd': 'bUryVn_O9_i_D9F7WOqEpA',
        'jazoest': '21915',
        '__spin_r': '1007805316',
        '__spin_b': 'trunk',
        '__spin_t': '1688761899',
        '__jssesw': '1',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'BarcelonaPostPageQuery',
        'variables': '{"postID":"3141737961795561608"}',
        'server_timestamps': 'true',
        'doc_id': '6529829603744567',
    }
        

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                try:
                    text = await response.text()
                    data = json.loads(text)
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    raise Exception('Failed to decode response as JSON')

        threads = data['data']['data']
        return threads

    async def __post_with_image(self, caption: str, image_path: str) -> bool:
        print("TEST")
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
                print("[ERROR] fail to file load: ", e)
                return None

        image_content = None
        if not (os.path.isfile(image_path) and os.path.exists(image_path)):
            if not await __is_valid_url(image_path):
                return False
            else:
                image_content = await __download(image_path)

        content = await self.upload_image(image_path, image_content=image_content)
        if content is not None:
            try:
                content = json.loads(content)
                upload_id = content["upload_id"]
                headers = {
                "authority": "www.threads.net",
                "accept": "*/*",
                "accept-language": "ko,en;q=0.9,ko-KR;q=0.8,ja;q=0.7",
                "cache-control": "no-cache",
                "origin": "https://www.threads.net",
                "pragma": "no-cache",
                "referer": f"https://www.threads.net/@{self.username}",
                "x-asbd-id": "129477",
                "x-fb-lsd": self.fbLSDToken,
                "x-ig-app-id": "238260118697367",
                }
                headers.update({"Authorization": f"Bearer IGT:2:{self.token}"})
                params = json.dumps(
                    {
                        "text_post_app_info": '{"reply_control":0}',
                        "scene_capture_type": "",
                        "timezone_offset": "-25200",
                        "source_type": "4",
                        "_uid": self.user_id,
                        "device_id": f"android-{random.randint(0, 1e24):x}",
                        "caption": caption,
                        "upload_id": upload_id,
                        "device": {
                            "manufacturer": "OnePlus",
                            "model": "ONEPLUS+A3010",
                            "android_version": 25,
                            "android_release": "7.1.1",
                        },
                    }
                )
                payload = f"signed_body=SIGNATURE.{urllib.parse.quote(params)}"

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url="https://i.instagram.com/api/v1/media/configure_text_post_app_feed/",
                        headers=headers,
                        data=payload,
                    ) as response:
                        text = await response.text()
                        post_result = json.loads(text)
                        if "status" in post_result.keys() and post_result["status"] == "ok":
                            return True
                        else:
                            raise Exception("Received a bad response")

            except Exception as e:
                print("[ERROR] ", e)
                print(traceback.format_exc())
                raise
        else:
            return False

    async def upload_image(self, image_url: str, image_content: bytes) -> str:
        headers = {
                "authority": "www.threads.net",
                "accept": "*/*",
                "accept-language": "ko,en;q=0.9,ko-KR;q=0.8,ja;q=0.7",
                "cache-control": "no-cache",
                "origin": "https://www.threads.net",
                "pragma": "no-cache",
                "referer": f"https://www.threads.net/@{self.username}",
                "x-asbd-id": "129477",
                "x-fb-lsd": self.fbLSDToken,
                "x-ig-app-id": "238260118697367",
                }
        headers.update({"Authorization": f"Bearer IGT:2:{self.token}"})

        upload_id = int(time.time() * 1000)
        name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"
        url = "https://www.instagram.com/rupload_igphoto/" + name

        if image_content is None:
            with open(image_url, mode="rb") as f:
                content = f.read()
            mime_type, _ = mimetypes.guess_type(image_url)
        else:
            content = image_content
            response = requests.head(image_url)
            content_type = response.headers.get("Content-Type")
            if not content_type:
                file_name = url.split("/")[-1]
                mime_type, _ = mimetypes.guess_type(file_name)

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
        contentLength = len(content)
        if mime_type.startswith("image/"):
            mime_type = mime_type.replace("image/", "")
        image_headers = {
            "X_FB_PHOTO_WATERFALL_ID": str(uuid.uuid4()),
            "X-Entity-Type": "image/" + mime_type,
            "Offset": "0",
            "X-Instagram-Rupload-Params": json.dumps(x_instagram_rupload_params),
            "X-Entity-Name": f"{name}",
            "X-Entity-Length": f"{contentLength}",
            "Content-Type": "application/octet-stream",
            "Content-Length": f"{contentLength}",
            "Accept-Encoding": "gzip",
        }

        headers.update(image_headers)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=content) as response:
                if response.status == 200:
                    text = await response.text()
                    print(text)
                    return text
                else:
                    print(response)
                    raise Exception("Failed to upload image")
                
    async def post(self, caption: str, image_path=None) -> bool:
        if self.user_id is None:
            raise Exception("Failed to resolve user_id. You must login to post posts")

        if self.token is None:
            raise Exception("Failed to resolve token. You must login to post posts")

        if image_path is not None:
            return await self.__post_with_image(caption=caption,image_path=image_path)

        params = json.dumps(
            {
                "publish_mode": "text_post",
                "text_post_app_info": '{"reply_control":0}',
                "timezone_offset": "-25200",
                "source_type": "4",
                "_uid": self.user_id,
                "device_id": f"android-{random.randint(0, 1e24):x}",
                "caption": caption,
                "upload_id": str(int(datetime.now().timestamp() * 1000)),
                "device": {
                    "manufacturer": "OnePlus",
                    "model": "ONEPLUS+A3010",
                    "android_version": 25,
                    "android_release": "7.1.1",
                },
            }
        )
        POST_HEADERS_DEFAULT = {
            "User-Agent": "Barcelona 289.0.0.77.109 Android",
            "Sec-Fetch-Site": "same-origin",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        payload = f"signed_body=SIGNATURE.{urllib.parse.quote(params)}"
        headers = POST_HEADERS_DEFAULT.copy()
        headers.update({"Authorization": f"Bearer IGT:2:{self.token}"})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://i.instagram.com/api/v1/media/configure_text_only_post/", headers=headers, data=payload) as response:
                    print(response)
                    if response.status == 200:
                        return True
                    else:
                        return False
        except Exception as e:
            print("[ERROR] ", e)
            return False
        
    def __get_app_headers(self) -> dict:
        headers = {
            "User-Agent": f"Barcelona 289.0.0.77.109 Android",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        if self.token is not None:
            headers["Authorization"] = f"Bearer IGT:2:{self.token}"
        return headers
    
    async def publish(
        self, caption: str, image_path: str = None, url: str = None, parent_post_id: str = None
    ) -> bool:
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
                print("[ERROR] fail to file load: ", e)
                return None
            
        print(self.token, self.user_id)

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
        post_url = "https://i.instagram.com/api/v1/media/configure_text_only_post/"
        if image_path is not None:
            post_url = "https://i.instagram.com/api/v1/media/configure_text_post_app_feed/"
            image_content = None
            if not (os.path.isfile(image_path) and os.path.exists(image_path)):
                if not __is_valid_url(image_path):
                    return False
                else:
                    image_content = await __download(image_path)
            upload_id = await self.upload_image(image_url=image_path, image_content=image_content)
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
        headers = self.__get_app_headers().copy()
        print("TEST")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(post_url, headers=headers, data=payload) as response:
                    print(response)
                    if response.status == 200:
                        return True
                    else:
                        return False
        except Exception as e:
            print("[ERROR] ", e)
            return False

    def publish_with_image(self, caption: str, image_path: str) -> bool:
        """
        @@deprecated
        Returns publish post with image

        Args:
            caption (str): post_id which is unique to each post.
            image_path (str): image path

        Returns:
            bool: verify that the post with image went publish
        """
        return self.publish(caption=caption, image_path=image_path)

    async def upload_image(self, image_url: str, image_content: bytes) -> str:
        headers = self.__get_app_headers().copy()

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
                    return None
