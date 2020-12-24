# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thoas/Sites/Python/ulule/python-mangopay/tests/__init__.py
# Compiled at: 2015-06-08 06:37:42
import mangopay
from . import settings
mangopay.client_id = settings.MANGOPAY_CLIENT_ID
mangopay.passphrase = settings.MANGOPAY_PASSPHRASE