# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/upnp_url.py
# Compiled at: 2018-09-01 22:23:46
try:
    from urlparse import urljoin
except Exception:
    from urllib.parse import urljoin