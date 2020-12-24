# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Token.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 3503 bytes
from re import search, I
from time import sleep
from xsrfprobe.files import config
from xsrfprobe.core.colors import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files import discovered
from urllib.parse import urlencode, unquote
from xsrfprobe.files.paramlist import COMMON_CSRF_NAMES, COMMON_CSRF_HEADERS

def Token(req, headers):
    """
    This method checks for whether Anti-CSRF Tokens are
               present in the request.
    """
    verbout(color.RED, '\n +---------------------------+')
    verbout(color.RED, ' |   Anti-CSRF Token Check   |')
    verbout(color.RED, ' +---------------------------+\n')
    param = ''
    query = ''
    found = False
    if config.TOKEN_CHECKS:
        verbout(O, 'Parsing request for detecting anti-csrf tokens...')
        try:
            con = unquote(urlencode(req)).split('&')
            for c in con:
                for name in COMMON_CSRF_NAMES:
                    qu = c.split('=')
                    if name.lower() in qu[0].lower():
                        verbout(color.GREEN, ' [+] The form was requested with an ' + color.BG + ' Anti-CSRF Token ' + color.END + color.GREEN + '!')
                        verbout(color.GREY, ' [+] Token Parameter: ' + color.CYAN + qu[0] + '=' + color.ORANGE + qu[1])
                        query, param = qu[0], qu[1]
                        discovered.REQUEST_TOKENS.append(param)
                        found = True
                        break

            if not found:
                for key, value in headers.items():
                    for name in COMMON_CSRF_HEADERS:
                        if name.lower() in key.lower():
                            verbout(color.GREEN, ' [+] The form was requested with an ' + color.BG + ' Anti-CSRF Token Header ' + color.END + color.GREEN + '!')
                            verbout(color.GREY, ' [+] Token Parameter: ' + color.CYAN + qu[0] + '=' + color.ORANGE + qu[1])
                            query, param = key, value
                            discovered.REQUEST_TOKENS.append(param)
                            break

        except Exception as e:
            verbout(R, 'Request Parsing Exception!')
            verbout(R, 'Error: ' + e.__str__())

        if param:
            return (query, param)
        else:
            verbout(color.ORANGE, ' [-] The form was requested ' + color.RED + ' Without an Anti-CSRF Token ' + color.END + color.ORANGE + '...')
            print(color.RED + ' [-] Endpoint seems ' + color.BR + ' VULNERABLE ' + color.END + color.RED + ' to ' + color.BR + ' POST-Based Request Forgery ' + color.END)
            return (None, None)