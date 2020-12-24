# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Cookie.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 7978 bytes
import time, os, sys
from re import search, I
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.request import Get
from xsrfprobe.core.randua import RandomAgent
from xsrfprobe.modules.Persistence import Persistence
from xsrfprobe.core.logger import VulnLogger, NovulLogger
from urllib.parse import urlencode, unquote, urlsplit
resps = []

def SameSite(url):
    """
    This function parses and verifies the cookies with
                    SameSite Flags.
    """
    verbout(color.RED, '\n +------------------------------------+')
    verbout(color.RED, ' |   Cross Origin Cookie Validation   |')
    verbout(color.RED, ' +------------------------------------+\n')
    foundx1 = 0
    foundx2 = 0
    foundx3 = 0
    verbout(color.GREY, ' [+] Lets examine how server reacts to same referer...')
    gen_headers = HEADER_VALUES
    gen_headers['User-Agent'] = USER_AGENT if USER_AGENT else RandomAgent()
    verbout(GR, 'Setting Referer header same as host...')
    gen_headers['Referer'] = urlsplit(url).netloc
    if COOKIE_VALUE:
        gen_headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
    getreq = Get(url, headers=gen_headers)
    map(HEADER_VALUES.pop, ['Referer', 'Cookie'])
    head = getreq.headers
    for h in head:
        if 'Cookie'.lower() in h.lower():
            verbout(G, 'Found cookie header value...')
            cookieval = head[h]
            verbout(color.ORANGE, ' [+] Cookie Received: ' + color.CYAN + str(cookieval))
            m = cookieval.split(';')
            verbout(GR, 'Examining Cookie...')
            for q in m:
                if search('SameSite', q, I):
                    verbout(G, 'SameSite Flag ' + color.ORANGE + ' detected on cookie!')
                    foundx1 = 1
                    q = q.split('=')[1].strip()
                    verbout(C, 'Cookie: ' + color.ORANGE + q)
                    break

        else:
            foundx3 = 2

    if foundx1 == 1:
        verbout(R, ' [+] Endpoint ' + color.ORANGE + 'SameSite Flag Cookie Validation' + color.END + ' Present!')
    verbout(color.GREY, ' [+] Lets examine how server reacts to a fake external referer...')
    gen_headers = HEADER_VALUES
    gen_headers['User-Agent'] = USER_AGENT if USER_AGENT else RandomAgent()
    gen_headers['Referer'] = REFERER_URL
    gen_headers.pop('Cookie', None)
    getreq = Get(url, headers=gen_headers)
    HEADER_VALUES.pop('Referer', None)
    head = getreq.headers
    for h in head:
        if 'Cookie'.lower() in h.lower():
            verbout(G, 'Found cookie header value...')
            cookieval = head[h]
            verbout(color.ORANGE, ' [+] Cookie Received: ' + color.CYAN + str(cookieval))
            m = cookieval.split(';')
            verbout(GR, 'Examining Cookie...')
            for q in m:
                if search('SameSite', q, I):
                    verbout(G, 'SameSite Flag ' + color.ORANGE + ' detected on cookie!')
                    foundx2 = 1
                    q = q.split('=')[1].strip()
                    verbout(C, 'Cookie: ' + color.ORANGE + q)
                    break

        else:
            foundx3 = 2

    if foundx1 == 1:
        verbout(R, ' [+] Endpoint ' + color.ORANGE + 'SameSite Flag Cookie Validation' + color.END + ' Present!')
    verbout(color.GREY, ' [+] Lets examine how server reacts to valid cookie from a different referer...')
    gen_headers = HEADER_VALUES
    gen_headers['User-Agent'] = USER_AGENT or RandomAgent()
    gen_headers['Referer'] = REFERER_URL
    if COOKIE_VALUE:
        gen_headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
    getreq = Get(url, headers=gen_headers)
    HEADER_VALUES.pop('Referer', None)
    head = getreq.headers
    for h in head:
        if 'Cookie'.lower() in h.lower():
            verbout(G, 'Found cookie header value...')
            cookieval = head[h]
            verbout(color.ORANGE, ' [+] Cookie Received: ' + color.CYAN + str(cookieval))
            m = cookieval.split(';')
            verbout(GR, 'Examining Cookie...')
            for q in m:
                if search('samesite', q.lower(), I):
                    verbout(G, 'SameSite Flag ' + color.ORANGE + ' detected on cookie on Cross Origin Request!')
                    foundx3 = 1
                    q = q.split('=')[1].strip()
                    verbout(C, 'Cookie: ' + color.ORANGE + q)
                    break

        else:
            foundx3 = 2

    if foundx1 == 1:
        verbout(R, 'Endpoint ' + color.ORANGE + 'SameSite Flag Cookie Validation' + color.END + ' is Present!')
    elif foundx1 == 1:
        if foundx3 == 0 and (foundx2 == 0 or foundx2 == 1):
            print(color.GREEN + ' [+] Endpoint ' + color.BG + ' NOT VULNERABLE to ANY type of CSRF attacks! ' + color.END)
            print(color.GREEN + ' [+] Protection Method Detected : ' + color.BG + ' SameSite Flag on Cookies ' + color.END)
            NovulLogger(url, 'SameSite Flag set on Cookies on Cross-Origin Requests.')
            oq = input(color.BLUE + ' [+] Continue scanning? (y/N) :> ')
            if oq.lower().startswith('n'):
                sys.exit('\n' + R + 'Shutting down XSRFProbe...\n')
        else:
            if foundx1 == 2:
                if foundx2 == 2 and foundx3 == 2:
                    print(color.GREEN + ' [+] Endpoint ' + color.BG + ' NOT VULNERABLE ' + color.END + color.GREEN + ' to CSRF attacks!')
                    print(color.GREEN + ' [+] Type: ' + color.BG + ' No Cookie Set while Cross Origin Requests ' + color.END)
                    NovulLogger(url, 'No cookie set on Cross-Origin Requests.')
    else:
        verbout(R, 'Endpoint ' + color.ORANGE + 'Cross Origin Cookie Validation' + color.END + ' Not Present!')
        verbout(R, 'Heuristic(s) reveal endpoint might be ' + color.BY + ' VULNERABLE ' + color.END + ' to CSRFs...')
        print(color.CYAN + ' [+] Possible CSRF Vulnerability Detected : ' + color.GREY + url + '!')
        print(color.ORANGE + ' [!] Possible Vulnerability Type: ' + color.BY + ' No Cross Origin Cookie Validation Presence ' + color.END)
        VulnLogger(url, 'No Cookie Validation on Cross-Origin Requests.', '[i] Headers: ' + str(head))


def Cookie(url, request):
    """
    This module is for checking the varied HTTP Cookies
            and the related security on them to
                    prevent CSRF attacks.
    """
    verbout(GR, 'Proceeding for cookie based checks...')
    SameSite(url)
    Persistence(url, request)