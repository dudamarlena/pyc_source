# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parosm/parse/parsemulti.py
# Compiled at: 2018-04-09 15:39:01
# Size of source mod 2**32: 1063 bytes
import os.path, magic
from parosm.parse.parsebase import BaseParser
from parosm.parse.parsepbf import PBFParser
from parosm.parse.parsexml import XMLParser

class MultiParser(BaseParser):

    def __init__(self, file, callback=None):
        super().__init__(file, callback)
        self._MultiParser__file = file
        if not os.path.isfile(file):
            raise Exception('is not a file')
        self._MultiParser__callback = self._MultiParser__default_callback if callback is None else callback
        file_type = magic.from_file(file)
        if file_type == 'OpenStreetMap XML data':
            self._MultiParser__parser = XMLParser(self._MultiParser__file, self._MultiParser__callback)
        else:
            if file_type == 'OpenStreetMap Protocolbuffer Binary Format':
                self._MultiParser__parser = PBFParser(self._MultiParser__file, self._MultiParser__callback)
            else:
                raise Exception('Not a osm file')

    @staticmethod
    def __default_callback(element):
        print(str(element))

    def parse(self):
        self._MultiParser__parser.parse()