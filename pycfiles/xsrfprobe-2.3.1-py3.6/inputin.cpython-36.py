# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/inputin.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2370 bytes
import socket, requests, re
from urllib.parse import urlparse
from xsrfprobe.core.colors import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files.dcodelist import IP
from xsrfprobe.core.logger import ErrorLogger
from xsrfprobe.files.config import SITE_URL, CRAWL_SITE, VERIFY_CERT

def inputin():
    """
    This module actually parses the url passed by the user.
    """
    if SITE_URL:
        web = SITE_URL
    else:
        if 'http' not in web:
            web = 'http://' + web
        try:
            web0 = urlparse(web).netloc
        except Exception:
            web0 = re.search(IP, web).group(0)

        try:
            print(O + 'Testing site ' + color.CYAN + web0 + color.END + ' status...')
            socket.gethostbyname(web0)
            print(color.GREEN + ' [+] Site seems to be up!' + color.END)
        except socket.gaierror:
            print(R + 'Site seems to be down...')
            quit()

        if not CRAWL_SITE:
            try:
                print(O + 'Testing ' + color.CYAN + web.split('//')[1].split('/', 1)[1] + color.END + ' endpoint status...')
                requests.get(web, verify=VERIFY_CERT)
                print(color.GREEN + ' [+] Endpoint seems to be up!' + color.END)
            except requests.exceptions.MissingSchema as e:
                verbout(R, 'Exception at: ' + color.GREY + web0)
                verbout(R, 'Error: Invalid URL Format')
                ErrorLogger(web0, e.__str__())
                quit()
            except requests.exceptions.HTTPError as e:
                verbout(R, 'HTTP Error: ' + web0)
                ErrorLogger(web0, e.__str__())
                quit()
            except requests.exceptions.ConnectionError as e:
                verbout(R, 'Connection Aborted: ' + web0)
                ErrorLogger(web0, e.__str__())
                quit()
            except Exception as e:
                verbout(R, 'Exception Caught: ' + e.__str__())
                ErrorLogger(web0, e.__str__())
                quit()

        web0 = web0.endswith('/') or web0 + '/'
    if web.split('//')[1] == web0:
        return (web, '')
    else:
        return (
         web, web0)