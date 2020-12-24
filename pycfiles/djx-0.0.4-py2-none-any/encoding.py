# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/utils/encoding.py
# Compiled at: 2019-02-14 00:35:06
import codecs, locale, re, sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List, Tuple, Text
BOMS = [(codecs.BOM_UTF8, 'utf8'),
 (
  codecs.BOM_UTF16, 'utf16'),
 (
  codecs.BOM_UTF16_BE, 'utf16-be'),
 (
  codecs.BOM_UTF16_LE, 'utf16-le'),
 (
  codecs.BOM_UTF32, 'utf32'),
 (
  codecs.BOM_UTF32_BE, 'utf32-be'),
 (
  codecs.BOM_UTF32_LE, 'utf32-le')]
ENCODING_RE = re.compile('coding[:=]\\s*([-\\w.]+)')

def auto_decode(data):
    """Check a bytes string for a BOM to correctly detect the encoding

    Fallback to locale.getpreferredencoding(False) like open() on Python3"""
    for bom, encoding in BOMS:
        if data.startswith(bom):
            return data[len(bom):].decode(encoding)

    for line in data.split('\n')[:2]:
        if line[0:1] == '#' and ENCODING_RE.search(line):
            encoding = ENCODING_RE.search(line).groups()[0].decode('ascii')
            return data.decode(encoding)

    return data.decode(locale.getpreferredencoding(False) or sys.getdefaultencoding())