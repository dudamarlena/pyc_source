# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/request.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 4473 bytes
import requests, time
from urllib.parse import urljoin
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.randua import RandomAgent
from xsrfprobe.files.discovered import FILES_EXEC
from xsrfprobe.core.logger import presheaders, preqheaders, ErrorLogger
headers = HEADER_VALUES
if COOKIE_VALUE:
    headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
if USER_AGENT_RANDOM:
    headers['User-Agent'] = RandomAgent()
if USER_AGENT:
    headers['User-Agent'] = USER_AGENT

def Post(url, action, data):
    """
    The main use of this function is as a
           Form Requester [POST].
    """
    global headers
    time.sleep(DELAY_VALUE)
    verbout(GR, 'Preparing the request...')
    if DISPLAY_HEADERS:
        preqheaders(headers)
    verbout(GR, 'Processing the ' + color.GREY + 'POST' + color.END + ' Request...')
    main_url = urljoin(url, action)
    try:
        response = requests.post(main_url, headers=headers, data=data, timeout=TIMEOUT_VALUE,
          verify=VERIFY_CERT)
        if DISPLAY_HEADERS:
            presheaders(response.headers)
        return response
    except requests.exceptions.HTTPError as e:
        verbout(R, 'HTTP Error : ' + main_url)
        ErrorLogger(main_url, e.__str__())
        return
    except requests.exceptions.ConnectionError as e:
        verbout(R, 'Connection Aborted : ' + main_url)
        ErrorLogger(main_url, e.__str__())
        return
    except requests.exceptions.ReadTimeout as e:
        verbout(R, 'Exception at: ' + color.GREY + url)
        verbout(R, 'Error: Read Timeout. Consider increasing the timeout value via --timeout.')
        ErrorLogger(url, e.__str__())
        return
    except ValueError as e:
        verbout(R, 'Value Error : ' + main_url)
        ErrorLogger(main_url, e.__str__())
        return
    except Exception as e:
        verbout(R, 'Exception Caught: ' + e.__str__())
        ErrorLogger(main_url, e.__str__())
        return


def Get(url, headers=headers):
    """
    The main use of this function is as a
            Url Requester [GET].
    """
    time.sleep(DELAY_VALUE)
    if url.split('.')[(-1)].lower() in (FILE_EXTENSIONS or EXECUTABLES):
        FILES_EXEC.append(url)
        verbout(G, 'Found File: ' + color.BLUE + url)
        return
    try:
        verbout(GR, 'Preparing the request...')
        if DISPLAY_HEADERS:
            preqheaders(headers)
        verbout(GR, 'Processing the ' + color.GREY + 'GET' + color.END + ' Request...')
        req = requests.get(url, headers=headers, timeout=TIMEOUT_VALUE, stream=False,
          verify=VERIFY_CERT)
        if DISPLAY_HEADERS:
            presheaders(req.headers)
        return req
    except requests.exceptions.MissingSchema as e:
        verbout(R, 'Exception at: ' + color.GREY + url)
        verbout(R, 'Error: Invalid URL Format')
        ErrorLogger(url, e.__str__())
        return
    except requests.exceptions.ReadTimeout as e:
        verbout(R, 'Exception at: ' + color.GREY + url)
        verbout(R, 'Error: Read Timeout. Consider increasing the timeout value via --timeout.')
        ErrorLogger(url, e.__str__())
        return
    except requests.exceptions.HTTPError as e:
        verbout(R, 'HTTP Error Encountered : ' + url)
        ErrorLogger(url, e.__str__())
        return
    except requests.exceptions.ConnectionError as e:
        verbout(R, 'Connection Aborted : ' + url)
        ErrorLogger(url, e.__str__())
        return
    except Exception as e:
        verbout(R, 'Exception Caught: ' + e.__str__())
        ErrorLogger(url, e.__str__())
        return