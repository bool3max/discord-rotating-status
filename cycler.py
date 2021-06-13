#!/usr/bin/python3

import itertools, json, sys
from time import sleep
import urllib.request as req
import urllib.error

ACC_TOKEN = sys.argv[1]
STATUS_URL = "https://discordapp.com/api/v6/users/@me/settings"  

DELAY_SEC = 1

req_headers = {
    "authorization": ACC_TOKEN,
    "Content-Type": "application/json",
    # requests lib inserts these by default....
    "User-Agent": "python-requests/2.25.1",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

for combo in itertools.cycle(sys.argv[2:]):
    # combo is in the form of <status_text>:<emoji_name>:<emoji_id>, and only the first part (<status_text>) is required
    parts = combo.split(':')
    req_data = {
        "custom_status": {
            "text": parts[0]
         }
    }

    if len(parts) == 2:
        req_data["custom_status"]["emoji_name"] = parts[1]

    if len(parts) == 3:
        req_data["custom_status"]["emoji_id"] = parts[2]

    raw_data = bytes(json.dumps(req_data), encoding='utf-8') # further encode json-encoded dictionary to UTF-8 byte object

    try:
        req_object = req.Request(STATUS_URL, headers = req_headers | {'Content-Length': len(raw_data)}, method = 'PATCH')
        req.urlopen(req_object, data=raw_data)
    except urllib.error.URLError as error:
        print(f"URLError: {error.reason}", file=sys.stderr)
        DELAY_SEC += 1
    else:
        if DELAY_SEC > 1:
            DELAY_SEC = 1

    sleep(DELAY_SEC)
