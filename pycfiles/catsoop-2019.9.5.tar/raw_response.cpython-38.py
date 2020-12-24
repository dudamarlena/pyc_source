# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__HANDLERS__/raw_response/raw_response.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 989 bytes


def handle(context):
    content = context['response']
    typ = context.get('content_type', 'text/plain')
    headers = {'Content-type':typ,  'Content-length':str(len(content))}
    return (('200', 'OK'), headers, content)