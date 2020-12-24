# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/ofxclient/util.py
# Compiled at: 2016-03-02 16:37:18
from __future__ import absolute_import
from __future__ import unicode_literals
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from ofxclient.client import Client

def combined_download(accounts, days=60):
    """Download OFX files and combine them into one

    It expects an 'accounts' list of ofxclient.Account objects
    as well as an optional 'days' specifier which defaults to 60
    """
    client = Client(institution=None)
    out_file = StringIO()
    out_file.write(client.header())
    out_file.write(b'<OFX>')
    for a in accounts:
        ofx = a.download(days=days).read()
        stripped = ofx.partition(b'<OFX>')[2].partition(b'</OFX>')[0]
        out_file.write(stripped)

    out_file.write(b'</OFX>')
    out_file.seek(0)
    return out_file