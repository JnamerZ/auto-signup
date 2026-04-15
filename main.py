#!/bin/python3

import argparse
from requests import post

auth_url = 'http://121.40.111.236:3033/api/auth/login'
checkin_url = 'http://121.40.111.236:3033/api/attendance/check-in'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5',
           'Connection': 'close',
           'Origin': 'http://121.40.111.236:3033',
           'Referer': 'http://121.40.111.236:3033/login',
           'Priority': 'u=0'
        }

def auth(username : str, password : str):
    global auth_url, headers
    resp = post(auth_url, headers=headers, json={"student_no": username, "password": password})
    data = resp.json().get("data")
    if data is None:
        return None
    return data.get("token")

def checkin(token : str):
    global checkin_url, headers
    ret, exception = 0, ''
    auth_headers = headers.copy()
    auth_headers['Authorization'] = f"Bearer {token}"
    resp = post(checkin_url, headers=auth_headers, json={'status': "在校"})
    if resp.json().get("code") != 200:
        ret = 1
        exception = str(resp.json())
    return ret, exception

def main():
    parser = argparse.ArgumentParser(
        description="Please provide your credential in arguments."
    )
    parser.add_argument("-u", dest="username", type=str, help="Your student number")
    parser.add_argument("-p", dest="password", type=str, help="Your password")
    parser.add_argument('--no-output', dest='stdnull', action='store_true', help="Disable any outputs")

    args = parser.parse_args()

    if args.username is None or args.password is None:
        parser.print_help()
        return -2

    token = auth(args.username, args.password)
    if token is None:
        if not args.stdnull: print("Login failed")
        return -1

    result, exception = checkin(token)
    if result:
        if not args.stdnull: print(f"Auto-check-in failed, error response: {exception}")
        return -1
    if not args.stdnull: print("Success")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
