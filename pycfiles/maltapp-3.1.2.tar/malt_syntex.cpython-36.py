# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_syntex.py
# Compiled at: 2017-05-12 18:31:42
# Size of source mod 2**32: 589 bytes
import malt
try:
    import syntex
except ImportError:
    syntex = None

if syntex:

    @malt.renderers.register('stx')
    def render(text):
        return syntex.render(text, pygmentize=True)