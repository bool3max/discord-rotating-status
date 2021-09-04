#!/usr/bin/python3

import sys, base64, itertools, json
import urllib.request as req
import urllib.error
from pathlib import Path
from time import sleep

REQUEST_URL = "https://discord.com/api/v9/users/@me"

def main():
    if len(sys.argv) < 4:
        print("Error: less than 3 arguments provided", file=sys.stderr)
        return 1

    ACC_TOKEN = sys.argv[1]
    PFP_PATH = sys.argv[2]
    CYCLE_INTERVAL = int(sys.argv[3])

    base_request_headers = {
        "authorization": ACC_TOKEN,
        "content-type": "application/json",
        "User-Agent": "python-requests/2.25.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # build an array of base64 strings corresponding the images in the given path
    b64_strings = []
    for image_path in Path(PFP_PATH).iterdir():
        with open(image_path, 'rb') as f:
            b64_strings.append(str(base64.b64encode(f.read()), encoding="utf-8"))

    for base64_imagedata in itertools.cycle(b64_strings):
        request_data = {
            "avatar": "data:image/png;base64," + base64_imagedata
        }

        raw_request_data = bytes(json.dumps(request_data), encoding="utf-8")
        base_request_headers["content-length"] = len(raw_request_data)

        request_object = req.Request(REQUEST_URL, headers = base_request_headers, method = "PATCH")

        print(f"Attempting request with 'content-length' of {base_request_headers['content-length']}")
        try:
            req.urlopen(request_object, data = raw_request_data)
        except urllib.error.URLError as error:
            # catch and print the error but don't increase the cycle interval
            print(f"Request failed: URLError: {error.reason}", file=sys.stderr)

        sleep(CYCLE_INTERVAL)


if __name__ == "__main__":
    exit(main())
