# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thoas/Sites/Python/ulule/python-mangopay/tests/resources.py
# Compiled at: 2015-06-08 06:37:42
from . import settings
from mangopay.api import APIRequest
handler = APIRequest(client_id=settings.MANGOPAY_CLIENT_ID, passphrase=settings.MANGOPAY_PASSPHRASE, sandbox=settings.MANGOPAY_USE_SANDBOX)
from mangopay.resources import *