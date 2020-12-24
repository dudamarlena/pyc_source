# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/api/utils.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals

def parse_mimetype(mime_type):
    """Parse the mime type in to it's component parts."""
    types = mime_type.split(b';')[0].split(b'/')
    ret_val = {b'type': mime_type, 
       b'main_type': types[0], 
       b'sub_type': types[1]}
    sub_type = types[1].split(b'+')
    ret_val[b'vendor'] = b''
    if len(sub_type) == 1:
        ret_val[b'format'] = sub_type[0]
    else:
        ret_val[b'format'] = sub_type[1]
        ret_val[b'vendor'] = sub_type[0]
    vendor = ret_val[b'vendor'].split(b'.')
    if len(vendor) > 1:
        ret_val[b'resource'] = vendor[(-1)].replace(b'-', b'_')
    else:
        ret_val[b'resource'] = b''
    return ret_val


def rem_mime_format(mime_type):
    """Strip the subtype from a mimetype, leaving vendor specific information.

    Removes the portion of the subtype after a +, or the entire
    subtype if no vendor specific type information is present.
    """
    if mime_type.rfind(b'+') != 0:
        return mime_type.rsplit(b'+', 1)[0]
    else:
        return mime_type.rsplit(b'/', 1)[0]