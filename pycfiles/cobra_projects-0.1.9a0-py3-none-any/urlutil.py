# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/policytool/urlutil.py
# Compiled at: 2019-05-23 11:08:11


def get_host(url):
    return url.split('/')[2]


def get_path(url):
    if url is None:
        return
    else:
        return '/' + ('/').join(url.split('/')[3:])