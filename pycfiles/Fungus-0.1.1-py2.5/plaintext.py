# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/text/formats/plaintext.py
# Compiled at: 2009-02-07 06:48:50
"""Plain text decoder.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
import pyglet

class PlainTextDecoder(pyglet.text.DocumentDecoder):

    def decode(self, text, location=None):
        document = pyglet.text.document.UnformattedDocument()
        document.insert_text(0, text)
        return document