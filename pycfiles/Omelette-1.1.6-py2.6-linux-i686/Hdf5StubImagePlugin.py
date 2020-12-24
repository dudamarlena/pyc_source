# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/Hdf5StubImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
import Image, ImageFile
_handler = None

def register_handler(handler):
    global _handler
    _handler = handler


def _accept(prefix):
    return prefix[:8] == b'\x89HDF\r\n\x1a\n'


class HDF5StubImageFile(ImageFile.StubImageFile):
    format = 'HDF5'
    format_description = 'HDF5'

    def _open(self):
        offset = self.fp.tell()
        if not _accept(self.fp.read(8)):
            raise SyntaxError('Not an HDF file')
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
        raise IOError('HDF5 save handler not installed')
    _handler.save(im, fp, filename)
    return


Image.register_open(HDF5StubImageFile.format, HDF5StubImageFile, _accept)
Image.register_save(HDF5StubImageFile.format, _save)
Image.register_extension(HDF5StubImageFile.format, '.h5')
Image.register_extension(HDF5StubImageFile.format, '.hdf')