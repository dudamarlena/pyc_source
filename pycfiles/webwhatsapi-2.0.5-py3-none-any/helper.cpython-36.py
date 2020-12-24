# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mukulhase/Dev/github/webwhatsapp-scripts/webwhatsapi/helper.py
# Compiled at: 2018-05-27 06:05:33
# Size of source mod 2**32: 241 bytes
import six

def safe_str(text):
    if not text:
        return '(empty)'
    else:
        assert isinstance(text, six.string_types), 'obj is not a string: %r' % text
        if text:
            return str(text.encode('utf-8').decode('ascii', 'ignore'))
        return '(empty)'