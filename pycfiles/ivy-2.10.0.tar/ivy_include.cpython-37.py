# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_include.py
# Compiled at: 2020-04-04 05:06:35
# Size of source mod 2**32: 1044 bytes
import shortcodes, ivy, os

@shortcodes.register('include')
def handler(node, content, pargs, kwargs):
    if pargs:
        path = ivy.site.inc(pargs[0])
        if os.path.exists(path):
            with open(path) as (file):
                return file.read()
    return ''