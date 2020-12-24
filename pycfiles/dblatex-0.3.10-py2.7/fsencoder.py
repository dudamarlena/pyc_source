# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/xetex/fsencoder.py
# Compiled at: 2017-04-03 18:58:57
"""
Provide an encoder for a font specification configuration: the encoder is fed
with Unicode characters one by one and determines the needed font switches
between the preceding and the current character.
"""
import sys, re, xml.dom.minidom
from fontspec import UnicodeInterval
from fsconfig import FontSpecConfig

class FontSpecEncoder:
    """
    Encoder working with font specifications: it is fed
    with Unicode characters one by one and it inserts the needed font switches
    between the preceding and the current character.
    """

    def __init__(self, configuration):
        """
        Create a font specification encoder from the specified configuration
        file (file name or file-like object).
        """
        self._conf = FontSpecConfig(configuration)
        self._cur_fontspec = None
        self._ref_stack = [self._conf.default_fontspec]
        return

    def reset(self):
        self._cur_fontspec = self._conf.default_fontspec
        self._ref_stack = [self._conf.default_fontspec]

    def _switch_to(self, fontspec):
        """
        Insert the transition string, according to the newly selected
        fontspec and the previously selected fontspec
        """
        s = ''
        if fontspec == self._cur_fontspec:
            return fontspec.interchar()
        if self._cur_fontspec:
            s += self._cur_fontspec.exit()
        self._cur_fontspec = fontspec
        s += fontspec.enter()
        return s

    def _encode(self, char):
        """
        Select the fontspec matching the specified <char>, and switch to
        this font as current font.

        The principle to find out the fontspec is:
        - to find from the current font level a matching font
          (the current font leaf or the direct font children)
        - if no font is found try with the parent font, and so on,
          up to the default root font (that must exist).
        """
        fontspec = self._cur_fontspec or self._conf.default_fontspec
        print >> sys.stderr, 'Current:', fontspec.id
        fontspec = fontspec.match(char)
        while not fontspec:
            leaf = self._ref_stack.pop()
            fontspec = self._ref_stack[(-1)].match(char, excluded=leaf)

        if fontspec != self._ref_stack[(-1)]:
            self._ref_stack.append(fontspec)
        return self._switch_to(fontspec)

    def ignorechars(self, charset):
        """Characters to ignore in font selection (maintain the current one)"""
        intervals = [ UnicodeInterval().from_char(c) for c in charset ]
        self._conf.default_fontspec.add_ignored(intervals)

    def encode(self, char):
        """
        Return a string consisting of the specified character prepended by
        all necessary font switching commands.
        """
        return (
         self._encode(char), char)

    def stop(self):
        """
        Cleanly exit from the current fontspec
        """
        if self._cur_fontspec:
            s = self._cur_fontspec.exit()
            self._cur_fontspec = None
            return s
        else:
            return