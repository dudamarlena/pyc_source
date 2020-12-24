# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/ascii_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1218 bytes
import numpy as np
from .base_parser import BaseParser

class ASCIIParser(BaseParser):
    __doc__ = '\n        ASCII Parser\n    '
    description = 'ASCII data'
    mimetypes = ['text/plain']
    can_write = True

    @classmethod
    def get_last_line(cls, f):
        i = -1
        f.seek(0)
        for i, l in enumerate(f):
            pass

        return (
         i + 1, l)

    @classmethod
    def write(cls, filename, x, ys, header='', delimiter=',', **kwargs):
        """
            Writes the header to the first line, and will write x, y1, ..., yn
            rows for each column inside the x and ys arguments.
            Header argument should not include a newline, and can be a string or
            any iterable containing strings.
        """
        f = open(filename, 'w')
        if not isinstance(header, str):
            header = delimiter.join(header)
        f.write('%s\n' % header)
        np.savetxt(f, (np.insert(ys, 0, x, axis=0).transpose()), fmt='%.8f', delimiter=delimiter)
        f.close()