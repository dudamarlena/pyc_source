# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/__init__.py
# Compiled at: 2020-04-26 06:12:15
# Size of source mod 2**32: 467 bytes
"""
web2ldap application package

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

def cmp(val1, val2):
    """
    Workaround to have cmp() like in Python 2
    """
    return bool(val1 > val2) - bool(val1 < val2)