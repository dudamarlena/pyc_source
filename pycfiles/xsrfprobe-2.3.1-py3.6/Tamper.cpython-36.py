# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Tamper.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 7416 bytes
from re import search, I
from urllib.parse import urlencode, quote
from xsrfprobe.core.colors import *
from xsrfprobe.core.request import Post
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.utils import replaceStrIndex
from xsrfprobe.files.paramlist import TOKEN_ERRORS
from xsrfprobe.core.logger import VulnLogger, NovulLogger

def Tamper(url, action, req, body, query, para):
    """
    The main idea behind this is to tamper the Anti-CSRF tokens
          found and check the content length for related
                      vulnerabilities.
    """
    verbout(color.RED, '\n +---------------------------------------+')
    verbout(color.RED, ' |   Anti-CSRF Token Tamper Validation   |')
    verbout(color.RED, ' +---------------------------------------+\n')
    flagx1, destx1 = (0, 0)
    flagx2, destx2 = (0, 0)
    flagx3, destx3 = (0, 0)
    verbout(GR, 'Proceeding for CSRF attack via Anti-CSRF token tampering...')
    if para == '':
        return True
    else:
        value = '%s' % para
        copy = req
        verbout(GR, 'Tampering Token by ' + color.GREY + 'index replacement' + color.END + '...')
        if value[3] != 'a':
            tampvalx1 = replaceStrIndex(value, 3, 'a')
        else:
            tampvalx1 = replaceStrIndex(value, 3, 'x')
        verbout(color.BLUE, ' [+] Original Token: ' + color.CYAN + value)
        verbout(color.BLUE, ' [+] Tampered Token: ' + color.CYAN + tampvalx1)
        req[query] = tampvalx1
        resp = Post(url, action, req)
        if str(resp.status_code).startswith('2'):
            destx1 = 1
        if not any(search(s, resp.text, I) for s in TOKEN_ERRORS):
            destx2 = 1
        if len(body) == len(resp.text):
            destx3 = 1
        if destx1 == 1 and destx2 == 1 or destx3 == 1:
            verbout(color.RED, ' [-] Anti-CSRF Token tamper by ' + color.GREY + 'index replacement' + color.RED + ' returns valid response!')
            flagx1 = 1
            VulnLogger(url, 'Anti-CSRF Token tamper by index replacement returns valid response.', '[i] POST Query: ' + req.__str__())
        else:
            verbout(color.RED, ' [+] Token tamper in request does not return valid response!')
            NovulLogger(url, 'Anti-CSRF Token tamper by index replacement does not return valid response.')
        verbout(GR, 'Tampering Token by ' + color.GREY + 'index removal' + color.END + '...')
        tampvalx2 = replaceStrIndex(value, 3)
        verbout(color.BLUE, ' [+] Original Token: ' + color.CYAN + value)
        verbout(color.BLUE, ' [+] Tampered Token: ' + color.CYAN + tampvalx2)
        req[query] = tampvalx2
        resp = Post(url, action, req)
        if str(resp.status_code).startswith('2'):
            destx1 = 2
        if not any(search(s, resp.text, I) for s in TOKEN_ERRORS):
            destx2 = 2
        if len(body) == len(resp.text):
            destx3 = 2
        if destx1 == 2 and destx2 == 2 or destx3 == 2:
            verbout(color.RED, ' [-] Anti-CSRF Token tamper by ' + color.GREY + 'index removal' + color.RED + ' returns valid response!')
            flagx2 = 1
            VulnLogger(url, 'Anti-CSRF Token tamper by index removal returns valid response.', '[i] POST Query: ' + req.__str__())
        else:
            verbout(color.RED, ' [+] Token tamper in request does not return valid response!')
            NovulLogger(url, 'Anti-CSRF Token tamper by index removal does not return valid response.')
        verbout(GR, 'Tampering Token by ' + color.GREY + 'Token removal' + color.END + '...')
        del req[query]
        verbout(color.GREY, ' [+] Removed token parameter from request!')
        resp = Post(url, action, req)
        if str(resp.status_code).startswith('2'):
            destx1 = 3
        if not any(search(s, resp.text, I) for s in TOKEN_ERRORS):
            destx2 = 3
        if len(body) == len(resp.text):
            destx3 = 3
        if destx1 == 3 and destx2 == 3 or destx3 == 3:
            verbout(color.RED, ' [-] Anti-CSRF' + color.GREY + ' Token removal' + color.RED + ' returns valid response!')
            flagx3 = 1
            VulnLogger(url, 'Anti-CSRF Token removal returns valid response.', '[i] POST Query: ' + req.__str__())
        else:
            verbout(color.RED, ' [+] Token tamper in request does not return valid response!')
            NovulLogger(url, 'Anti-CSRF Token removal does not return valid response.')
        if flagx1 == 1 and flagx2 == 1 or flagx1 == 1 and flagx3 == 1 or flagx2 == 1 and flagx3 == 1:
            verbout(color.RED, ' [+] The tampered token value works! Endpoint ' + color.BR + ' VULNERABLE to Replay Attacks ' + color.END + '!')
            verbout(color.ORANGE, ' [-] The Tampered Anti-CSRF Token requested does NOT return a 40x or 50x response! ')
            print(color.RED + ' [-] Endpoint ' + color.BR + ' CONFIRMED VULNERABLE ' + color.END + color.RED + ' to Request Forgery Attacks...')
            print(color.ORANGE + ' [!] Vulnerability Type: ' + color.BR + ' Non-Unique Anti-CSRF Tokens in Requests ' + color.END + '\n')
            VulnLogger(url, 'Anti-CSRF Tokens are not Unique. Token Reuse detected.', '[i] Request: ' + str(copy))
            return True
        print(color.RED + ' [-] The Tampered Anti-CSRF Token requested returns a 40x or 50x response... ')
        print(color.GREEN + ' [-] Endpoint ' + color.BG + ' NOT VULNERABLE ' + color.END + color.ORANGE + ' to CSRF Attacks...')
        print(color.ORANGE + ' [!] CSRF Mitigation Method: ' + color.BG + ' Unique Anti-CSRF Tokens ' + color.END + '\n')
        NovulLogger(url, 'Unique Anti-CSRF Tokens. No token reuse.')
        return False