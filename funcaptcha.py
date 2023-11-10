import base64
import hashlib
import json
import secrets

import execjs
from Crypto.Cipher import AES
import aiohttp
import asyncio

from urllib.parse import urlparse

import random, string, time

with open("fp.js") as f:
    mm3js = execjs.compile(f.read())

class funcaptcha:

    def __init__(
            self,
            service_url: str,
            public_key: str,
            site_url: str,
            user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            capi_version: str = "1.5.5",
            headers=None,
            proxy: str = None,
    ):
        if headers is None:
            headers = {}

        self.service_url = service_url
        self.public_key = public_key
        self.site_url = site_url
        self.capi_version = capi_version
        self.user_agent = user_agent
        self.proxy = proxy

        self.url = f"{self.service_url}/fc/gt2/public_key/{self.public_key}"

        default_headers = {
            'user-agent': self.user_agent,
            'authority': urlparse(self.url).netloc,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": self.service_url,
            "referer": f"{self.service_url}/v2/{self.capi_version}/enforcement.fbfc14b0d793c6ef8359e0e4b4a91f67.html",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }

        self.headers = {**default_headers, **headers}

    async def get_token(self):
        rnd = random.uniform(0, 1)
        bda = self._get_browser_data()

        data = {
            "bda": bda,
            "public_key": self.public_key,
            "site": self.site_url,
            "userbrowser": self.user_agent,
            "capi_version": self.capi_version,
            "capi_mode": "lightbox",
            "style_theme": "default",
            "simulate_rate_limit": 0,
            "simulated": 0,
            "rnd": rnd
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=data, proxy=self.proxy, ssl=False) as response:
                return await response.text()

    def _get_browser_data(self):
        ts = time.time()
        timeframe = int(ts - (ts % 21600))
        key = self.user_agent + str(timeframe)

        ## Data
        data = []
        data.append({"key": "api_type", "value": "js"})
        data.append({"key": "p", "value": 1})

        ## Fingerprint
        fonts = "Arial,Arial Black,Arial Narrow,Book Antiqua,Bookman Old Style,Calibri,Cambria,Cambria Math,Century,Century Gothic,Century Schoolbook,Comic Sans MS,Consolas,Courier,Courier New,Garamond,Georgia,Helvetica,Impact,Lucida Bright,Lucida Calligraphy,Lucida Console,Lucida Fax,Lucida Handwriting,Lucida Sans,Lucida Sans Typewriter,Lucida Sans Unicode,Microsoft Sans Serif,Monotype Corsiva,MS Gothic,MS PGothic,MS Reference Sans Serif,MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings,Wingdings 2,Wingdings 3".split(
            ",")
        plugins = "Chrome PDF Plugin,Chrome PDF Viewer,Native Client".split(",")
        canvas_fp = -1424337346

        fe = [
            ## DoNotTrack flag
            "DNT:unknown",
            ## Language
            "L:en-US",
            ## Depth
            "D:24",
            ## Pixel ratio
            "PR:1",
            ## Screen resolution
            "S:1920,1080",
            ## Available screen resolution (browser window size)
            "AS:1920,1040",
            ## Time offset
            "TO:-120",
            ## Session storage enabled
            "SS:true",
            ## Local storage enabled
            "LS:true",
            ## Indexed DB enabled
            "IDB:true",
            ## .addBehaviour enabled - https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms535922(v%3Dvs.85)
            "B:false",
            ## OpenDB enabled
            "ODB:true",
            ## CPU class
            "CPUC:unknown",
            ## Platform key
            "PK:Win32",
            ## Canvas fingerprint
            "CFP:" + str(canvas_fp),
            ## Has fake resolution
            "FR:false",
            ## Has fake OS
            "FOS:false",
            ## Has fake browser
            "FB:false",
            ## Javascript fonts
            "JSF:" + ",".join(fonts),
            ## Plugin keys
            "P:" + ",".join(plugins),
            ## Touch
            "T:0,false,false",
            ## navigator.hardwareConcurrency value
            "H:8",
            ## Flash enabled
            "SWF:false"]

        ## Calculate hashes
        ## I haven't managed to replicate fp hashes yet, so it's just filled with a random value for now
        fp = secrets.token_hex(16)
        ife_hash = mm3js.call("x64hash128", ", ".join(fe), 38)

        ## Window hash
        ## This cannot be verified by the server, so it's just a random value for now
        wh = secrets.token_hex(16) + "|" + secrets.token_hex(16)

        ## Additional data
        data.append({"key": "f", "value": fp})
        data.append({"key": "n", "value": base64.b64encode(str(int(ts)).encode("utf-8")).decode("utf-8")})
        data.append({"key": "wh", "value": wh})
        data.append({"key": "fe", "value": fe})
        data.append({"key": "ife_hash", "value": ife_hash})
        data.append({"key": "cs", "value": 1})
        data.append({"key": "jsbd", "value": '{"HL":28,"NCE":true,"DA":null,"DR":null,"DMT":31,"DO":null,"DOT":31}'})

        data = json.dumps(data, separators=(',', ':'))
        data = self._cryptojs_encrypt(data, key)
        data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        return data

    def _cryptojs_encrypt(self, data, key):
        # Padding
        data = data + chr(16 - len(data) % 16) * (16 - len(data) % 16)

        salt = b"".join(random.choice(string.ascii_lowercase).encode() for x in range(8))
        salted, dx = b"", b""
        while len(salted) < 48:
            dx = hashlib.md5(dx + key.encode() + salt).digest()
            salted += dx

        key = salted[:32]
        iv = salted[32:32 + 16]
        aes = AES.new(key, AES.MODE_CBC, iv)

        encrypted_data = {"ct": base64.b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(),
                          "s": salt.hex()}
        return json.dumps(encrypted_data, separators=(',', ':'))


if __name__ == "__main__":
    public_key = "0A1D34FC-659D-4E23-B17B-694DCFCF6A6C"
    service_url = "https://tcr9i.chat.openai.com"
    site_url = "https://auth0.openai.com"

    s = funcaptcha(
        public_key=public_key,
        service_url=service_url,
        site_url=site_url,
    )

    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(s.get_token()))

