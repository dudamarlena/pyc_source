# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/utils/encoding.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 1320 bytes
import codecs, locale, re, sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List, Tuple, Text
BOMS = [(codecs.BOM_UTF8, 'utf-8'),
 (
  codecs.BOM_UTF16, 'utf-16'),
 (
  codecs.BOM_UTF16_BE, 'utf-16-be'),
 (
  codecs.BOM_UTF16_LE, 'utf-16-le'),
 (
  codecs.BOM_UTF32, 'utf-32'),
 (
  codecs.BOM_UTF32_BE, 'utf-32-be'),
 (
  codecs.BOM_UTF32_LE, 'utf-32-le')]
ENCODING_RE = re.compile(b'coding[:=]\\s*([-\\w.]+)')

def auto_decode(data):
    """Check a bytes string for a BOM to correctly detect the encoding

    Fallback to locale.getpreferredencoding(False) like open() on Python3"""
    for bom, encoding in BOMS:
        if data.startswith(bom):
            return data[len(bom):].decode(encoding)

    for line in data.split(b'\n')[:2]:
        if line[0:1] == b'#':
            if ENCODING_RE.search(line):
                encoding = ENCODING_RE.search(line).groups()[0].decode('ascii')
                return data.decode(encoding)

    return data.decode(locale.getpreferredencoding(False) or sys.getdefaultencoding())