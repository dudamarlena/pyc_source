# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/common/msdos.py
# Compiled at: 2009-09-07 17:44:28
"""
MS-DOS structures.

Documentation:
- File attributes:
  http://www.cs.colorado.edu/~main/cs1300/include/ddk/winddk.h
"""
from hachoir_core.field import StaticFieldSet
from hachoir_core.field import Bit, NullBits
_FIELDS = (
 (
  Bit, 'read_only'), (Bit, 'hidden'), (Bit, 'system'), (NullBits, 'reserved[]', 1), (Bit, 'directory'), (Bit, 'archive'), (Bit, 'device'), (Bit, 'normal'), (Bit, 'temporary'), (Bit, 'sparse_file'), (Bit, 'reparse_file'), (Bit, 'compressed'), (Bit, 'offline'), (Bit, 'dont_index_content'), (Bit, 'encrypted'))

class MSDOSFileAttr16(StaticFieldSet):
    """
    MSDOS 16-bit file attributes
    """
    __module__ = __name__
    format = _FIELDS + ((NullBits, 'reserved[]', 1),)
    _text_keys = ('directory', 'read_only', 'compressed', 'hidden', 'system', 'normal',
                  'device', 'temporary', 'archive')

    def createValue(self):
        mode = []
        for name in self._text_keys:
            if self[name].value:
                if 4 <= len(mode):
                    mode.append('...')
                    break
                else:
                    mode.append(name)

        if mode:
            return (', ').join(mode)
        else:
            return '(none)'


class MSDOSFileAttr32(MSDOSFileAttr16):
    """
    MSDOS 32-bit file attributes
    """
    __module__ = __name__
    format = _FIELDS + ((NullBits, 'reserved[]', 17),)