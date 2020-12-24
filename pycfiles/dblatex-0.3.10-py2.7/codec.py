# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/xetex/codec.py
# Compiled at: 2017-04-03 18:58:57
import sys, os, codecs
from dbtexmf.dblatex.texcodec import LatexCodec
from fsencoder import FontSpecEncoder

class XetexCodec(LatexCodec):

    def __init__(self, fontconfig='', pre='', post=''):
        LatexCodec.__init__(self, input_encoding='utf8', output_encoding='utf8')
        if not fontconfig:
            fontconfig = os.getenv('DBLATEX_FONTSPEC_FILE', 'xefont.xml')
        try:
            self._fontmgr = FontSpecEncoder(fontconfig)
        except:
            self._fontmgr = None
            return

        self._fontmgr.ignorechars('\x01\x02\r')
        return

    def clear_errors(self):
        pass

    def get_errors(self):
        pass

    def decode(self, text):
        return self._decode(text)[0]

    def encode(self, text):
        if not self._fontmgr:
            return LatexCodec.encode(self, text)
        text = text.replace('\\', '\x02')
        self._fontmgr.reset()
        switchfonts = []
        for c in text:
            font, char = self._fontmgr.encode(c)
            if font or not switchfonts:
                sf = [
                 font, char]
                switchfonts.append(sf)
            else:
                sf[1] += char

        text = ''
        for sf in switchfonts:
            sf[1] = self._texescape(sf[1])
            text += ('').join(sf)

        text = self._encode(text)[0]
        text = text.replace('\x02', '\\textbackslash{}')
        return '{' + text + '}'