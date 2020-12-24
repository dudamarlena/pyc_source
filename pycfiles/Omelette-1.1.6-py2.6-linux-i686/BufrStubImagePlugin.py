# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/BufrStubImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
import Image, ImageFile
_handler = None

def register_handler(handler):
    global _handler
    _handler = handler


def _accept(prefix):
    return prefix[:4] == 'BUFR' or prefix[:4] == 'ZCZC'


class BufrStubImageFile(ImageFile.StubImageFile):
    format = 'BUFR'
    format_description = 'BUFR'

    def _open(self):
        offset = self.fp.tell()
        if not _accept(self.fp.read(8)):
            raise SyntaxError('Not a BUFR file')
        self.fp.seek(offset)
        self.mode = 'F'
        self.size = (1, 1)
        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler


def _save(im, fp, filename):
    if _handler is None or not hasattr('_handler', 'save'):
        raise IOError('BUFR save handler not installed')
    _handler.save(im, fp, filename)
    return


Image.register_open(BufrStubImageFile.format, BufrStubImageFile, _accept)
Image.register_save(BufrStubImageFile.format, _save)
Image.register_extension(BufrStubImageFile.format, '.bufr')