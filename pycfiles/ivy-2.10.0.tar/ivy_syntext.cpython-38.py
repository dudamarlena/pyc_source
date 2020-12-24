# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_syntext.py
# Compiled at: 2019-10-28 14:31:14
# Size of source mod 2**32: 418 bytes
import ivy
try:
    import syntext
except ImportError:
    pass
else:

    @ivy.renderers.register('stx', 'sxt')
    def render(text):
        return syntext.render(text, pygmentize=True)