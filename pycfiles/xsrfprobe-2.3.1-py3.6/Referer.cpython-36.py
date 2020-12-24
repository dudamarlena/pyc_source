# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Referer.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 3338 bytes
import requests
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.request import Get
from xsrfprobe.core.logger import VulnLogger, NovulLogger

def Referer(url):
    """
    Check if the remote web application verifies the Referer before
                    processing the HTTP request.
    """
    verbout(color.RED, '\n +--------------------------------------+')
    verbout(color.RED, ' |   Referer Based Request Validation   |')
    verbout(color.RED, ' +--------------------------------------+\n')
    verbout(O, 'Making request on normal basis...')
    req0x01 = Get(url)
    verbout(GR, 'Setting generic headers...')
    gen_headers = HEADER_VALUES
    gen_headers['Referer'] = REFERER_URL
    if COOKIE_VALUE:
        gen_headers['Cookie'] = ','.join(cookie for cookie in COOKIE_VALUE)
    verbout(O, 'Making request with ' + color.CYAN + 'Tampered Referer Header' + color.END + '...')
    req0x02 = Get(url, headers=gen_headers)
    HEADER_VALUES.pop('Referer', None)
    if len(req0x01.content) != len(req0x02.content):
        print(color.GREEN + ' [+] Endoint ' + color.ORANGE + 'Referer Validation' + color.GREEN + ' Present!')
        print(color.GREEN + ' [-] Heuristics reveal endpoint might be ' + color.BG + ' NOT VULNERABLE ' + color.END + '...')
        print(color.ORANGE + ' [+] Mitigation Method: ' + color.BG + ' Referer Based Request Validation ' + color.END)
        NovulLogger(url, 'Presence of Referer Header based Request Validation.')
        return True
    else:
        verbout(R, 'Endpoint ' + color.RED + 'Referer Validation Not Present' + color.END + '!')
        verbout(R, 'Heuristics reveal endpoint might be ' + color.BY + ' VULNERABLE ' + color.END + ' to Origin Based CSRFs...')
        print(color.CYAN + ' [+] Possible CSRF Vulnerability Detected : ' + color.GREY + url + '!')
        print(color.ORANGE + ' [+] Possible Vulnerability Type: ' + color.BY + ' No Referer Based Request Validation ' + color.END)
        VulnLogger(url, 'No Referer Header based Request Validation presence.', '[i] Response Headers: ' + str(req0x02.headers))
        return False