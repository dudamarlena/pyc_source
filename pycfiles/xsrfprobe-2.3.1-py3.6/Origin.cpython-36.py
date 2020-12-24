# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Origin.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 3371 bytes
import requests
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.request import Get
from xsrfprobe.core.randua import RandomAgent
from xsrfprobe.core.logger import VulnLogger, NovulLogger

def Origin(url):
    """
    Check if the remote web application verifies the Origin before
                    processing the HTTP request.
    """
    verbout(color.RED, '\n +-------------------------------------+')
    verbout(color.RED, ' |   Origin Based Request Validation   |')
    verbout(color.RED, ' +-------------------------------------+\n')
    verbout(O, 'Making request on normal basis...')
    req0x01 = Get(url)
    verbout(GR, 'Setting generic headers...')
    gen_headers = HEADER_VALUES
    gen_headers['Origin'] = ORIGIN_URL
    if COOKIE_VALUE:
        gen_headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
    verbout(O, 'Making request with ' + color.CYAN + 'Tampered Origin Header' + color.END + '...')
    req0x02 = Get(url, headers=gen_headers)
    HEADER_VALUES.pop('Origin', None)
    if len(req0x01.content) != len(req0x02.content):
        verbout(color.GREEN, ' [+] Endoint ' + color.ORANGE + 'Origin Validation' + color.GREEN + ' Present!')
        print(color.GREEN + ' [-] Heuristics reveal endpoint might be ' + color.BG + ' NOT VULNERABLE ' + color.END + '...')
        print(color.ORANGE + ' [+] Mitigation Method: ' + color.BG + ' Origin Based Request Validation ' + color.END + '\n')
        NovulLogger(url, 'Presence of Origin Header based request Validation.')
        return True
    else:
        verbout(R, 'Endpoint ' + color.RED + 'Origin Validation Not Present' + color.END + '!')
        verbout(R, 'Heuristics reveal endpoint might be ' + color.BY + ' VULNERABLE ' + color.END + ' to Origin Based CSRFs...')
        print(color.CYAN + ' [+] Possible CSRF Vulnerability Detected : ' + color.GREY + url + '!')
        print(color.ORANGE + ' [!] Possible Vulnerability Type: ' + color.BY + ' No Origin Based Request Validation ' + color.END + '\n')
        VulnLogger(url, 'No Origin Header based request validation presence.', '[i] Response Headers: ' + str(req0x02.headers))
        return False