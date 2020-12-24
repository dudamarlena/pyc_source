# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/client/common.py
# Compiled at: 2018-12-27 05:19:41
import requests
from russell.exceptions import RussellException
from base64 import b64encode
from russell.cli.utils import force_unicode

def get_url_contents(url):
    """
    Downloads the content of the url and returns it
    """
    response = requests.get(url)
    if response.status_code == 200:
        return force_unicode(response.content)
    raise RussellException(('Failed to get contents of the url : {}').format(url))


def get_basic_token(access_token):
    return b64encode(('{}:').format(access_token).encode()).decode('ascii')