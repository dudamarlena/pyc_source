# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-api/odnoklassniki_api/exceptions.py
# Compiled at: 2015-11-01 17:30:06


class OdnoklassnikiDeniedAccessError(Exception):
    pass


class OdnoklassnikiContentError(Exception):
    pass


class OdnoklassnikiParseError(Exception):
    pass