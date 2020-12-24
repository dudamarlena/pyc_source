# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Persistence.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 7614 bytes
import time, os, sys
from re import search, I
from datetime import datetime
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.request import Get
from xsrfprobe.core.randua import RandomAgent
from xsrfprobe.core.utils import checkDuplicates
from xsrfprobe.core.logger import VulnLogger, NovulLogger
from urllib.parse import urlencode, unquote, urlsplit
resps = []

def Persistence(url, postq):
    """
    The main idea behind this is to check for Cookie
                    Persistence.
    """
    verbout(color.RED, '\n +-----------------------------------+')
    verbout(color.RED, ' |   Cookie Persistence Validation   |')
    verbout(color.RED, ' +-----------------------------------+\n')
    verbout(GR, 'Proceeding to test for ' + color.GREY + 'Cookie Persistence' + color.END + '...')
    time.sleep(0.7)
    found = 0
    cookies = []
    verbout(C, 'Proceeding to test cookie persistence via ' + color.CYAN + 'Prepared GET Requests' + color.END + '...')
    verbout(GR, 'Making the request...')
    req = Get(url, headers=HEADER_VALUES)
    if req.cookies:
        for cook in req.cookies:
            if cook.expires:
                print(color.GREEN + ' [+] Persistent Cookies found in Response Headers!')
                print(color.GREY + ' [+] Cookie: ' + color.CYAN + cook.__str__())
                print(color.GREEN + ' [+] Cookie Expiry Period: ' + color.ORANGE + datetime.fromtimestamp(cook.expires).__str__())
                found = 1
                VulnLogger(url, 'Persistent Session Cookies Found.', '[i] Cookie: ' + req.headers.get('Set-Cookie'))
            else:
                NovulLogger(url, 'No Persistent Session Cookies.')

    if found == 0:
        verbout(R, 'No persistent session cookies identified on GET Type Requests!')
    verbout(C, 'Proceeding to test cookie persistence on ' + color.CYAN + 'POST Requests' + color.END + '...')
    if postq.cookies:
        for cookie in postq.cookies:
            if cookie.expires:
                print(color.GREEN + ' [+] Persistent Cookies found in Response Headers!')
                print(color.GREY + ' [+] Cookie: ' + color.CYAN + cookie.__str__())
                print(color.GREEN + ' [+] Cookie Expiry Period: ' + color.ORANGE + datetime.fromtimestamp(cookie.expires).__str__())
                found = 1
                VulnLogger(url, 'Persistent Session Cookies Found.', '[i] Cookie: ' + req.headers.get('Set-Cookie'))
                print(color.ORANGE + ' [!] Probable Insecure Practice: ' + color.BY + ' Persistent Session Cookies ' + color.END)
            else:
                NovulLogger(url, 'No Persistent Cookies.')

    if found == 0:
        verbout(R, 'No persistent session cookies identified upon POST Requests!')
        print(color.ORANGE + ' [+] Endpoint might be ' + color.BY + ' NOT VULNERABLE ' + color.END + color.ORANGE + ' to CSRF attacks!')
        print(color.ORANGE + ' [+] Detected : ' + color.BY + ' No Persistent Cookies ' + color.END)
    if found != 1:
        verbout(C, 'Proceeding to test cookie persistence via ' + color.CYAN + 'User-Agent Alteration' + color.END + '...')
        user_agents = {'Chrome on Windows 8.1':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36', 
         'Safari on iOS':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4', 
         'IE6 on Windows XP':'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)', 
         'Opera on Windows 10':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991', 
         'Chrome on Android':'Mozilla/5.0 (Linux; U; Android 2.3.1; en-us; MID Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
        verbout(GR, 'Setting custom generic headers...')
        gen_headers = HEADER_VALUES
        for name, agent in user_agents.items():
            verbout(C, 'Using User-Agent : ' + color.CYAN + name)
            verbout(GR, 'Value : ' + color.ORANGE + agent)
            gen_headers['User-Agent'] = agent
            if COOKIE_VALUE:
                gen_headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
            req = Get(url, headers=gen_headers)
            if req.headers.get('Set-Cookie'):
                resps.append(req.headers.get('Set-Cookie'))

        HEADER_VALUES.pop('User-Agent', None)
        HEADER_VALUES['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        if resps:
            if checkDuplicates(resps):
                verbout(G, 'Set-Cookie header does not change with varied User-Agents...')
                verbout(color.ORANGE, ' [+] Possible persistent session cookies found...')
                print(color.RED + ' [+] Possible CSRF Vulnerability Detected : ' + color.ORANGE + url + '!')
                print(color.ORANGE + ' [!] Probable Insecure Practice: ' + color.BY + ' Persistent Session Cookies ' + color.END)
                VulnLogger(url, 'Persistent Session Cookies Found.', '[i] Cookie: ' + req.headers.get('Set-Cookie'))
            else:
                verbout(G, 'Set-Cookie header changes with varied User-Agents...')
                verbout(R, 'No possible persistent session cookies found...')
                verbout(color.ORANGE, ' [+] Endpoint ' + color.BY + ' PROBABLY NOT VULNERABLE ' + color.END + color.ORANGE + ' to CSRF attacks!')
                verbout(color.ORANGE, ' [+] Application Practice Method Detected : ' + color.BY + ' No Persistent Cookies ' + color.END)
                NovulLogger(url, 'No Persistent Cookies.')
        else:
            verbout(R, 'No cookies are being set on any requests.')