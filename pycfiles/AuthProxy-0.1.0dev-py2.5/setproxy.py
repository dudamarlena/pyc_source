# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/lib/setproxy.py
# Compiled at: 2007-12-04 10:29:48
import os, urllib2

def set_proxy(url=None):
    if not url:
        return false
    proxy_support = urllib2.ProxyHandler({'http': url, 'https': url})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    return True