# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/policytool/urlutil.py
# Compiled at: 2019-05-23 11:08:11


def get_host(url):
    return url.split('/')[2]


def get_path(url):
    if url is None:
        return
    else:
        return '/' + ('/').join(url.split('/')[3:])