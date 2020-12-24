# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wuhanncov/lark.py
# Compiled at: 2020-01-29 03:32:34
import requests

def notify_lark(title=None, msg='', lark_url=''):
    url = lark_url
    if not url.startswith('http'):
        print 'lark webhook url not valid %s' % url
    if title is not None:
        payload = '{\n\n"title": "' + title + '",\n"text": "' + msg + '"\n\n} '
    else:
        payload = '{\n\n"text": "' + msg + '"\n\n} '
    headers = {'Content-Type': 'application/json'}
    payload = (' ').join([payload]).encode('utf-8').strip()
    requests.request('POST', url, headers=headers, data=payload)
    return