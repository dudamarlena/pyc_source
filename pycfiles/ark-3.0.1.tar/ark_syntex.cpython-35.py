# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_syntex.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 587 bytes
import ark
try:
    import syntex
except ImportError:
    syntex = None

if syntex:

    @ark.renderers.register('stx')
    def render(text):
        return syntex.render(text, pygmentize=True)