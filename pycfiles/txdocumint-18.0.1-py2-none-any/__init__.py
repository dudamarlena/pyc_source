# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathan/Coding/txdocumint/txdocumint/__init__.py
# Compiled at: 2018-07-02 07:13:04
from txdocumint._client import create_session, get_session
__all__ = [
 'create_session', 'get_session']
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions