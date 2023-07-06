import requests
from typing import Optional, Dict, Union, List
import aiohttp
import re
import json

class Extensions:
    # Define the Extensions class if necessary
    pass

class Thread:
    # Define the Thread class if necessary
    pass

class ThreadsUser:
    # Define the ThreadsUser class if necessary
    pass

class GetUserProfileResponse:
    def __init__(self, data: Dict[str, Union[Dict[str, Union[ThreadsUser, Dict[str, Union[str, int]]]], Extensions]]):
        self.data = data['data']
        self.extensions = data['extensions']

class GetUserProfileThreadsResponse:
    def __init__(self, data: Dict[str, Union[Dict[str, List[Thread]] , Extensions]]):
        self.data = data['data']
        self.extensions = data['extensions']

class ThreadsAPIOptions:
    def __init__(self, fbLSDToken: Optional[str] = None):
        self.fbLSDToken = fbLSDToken

class ThreadsAPI:
    def __init__(self, options: Optional[ThreadsAPIOptions] = None):
        self.fbLSDToken = 'NjppQDEgONsU_1LCzrmp6q'  # FIXME: Remove default value
        if options and options.fbLSDToken:
            self.fbLSDToken = options.fbLSDToken

    def _get_default_headers(self, username: str) -> Dict[str, Union[str, int]]:
        return {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'ko',
            'cache-control': 'no-cache',
            'origin': 'https://www.threads.net',
            'pragma': 'no-cache',
            'referer': f'https://www.threads.net/@{username}',
            'x-asbd-id': '129477',
            'x-fb-lsd': self.fbLSDToken,
            'x-ig-app-id': '238260118697367',
        }

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