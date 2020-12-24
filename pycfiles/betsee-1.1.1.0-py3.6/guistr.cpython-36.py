# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/type/text/guistr.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2609 bytes
"""
Low-level Qt-specific string handling functionality.
"""
from PySide2.QtCore import Qt, QByteArray
from betse.util.type.text import mls
from betse.util.type.types import type_check

@type_check
def is_rich(text: str) -> bool:
    """
    ``True`` only if the passed text superficially appears to be HTML and thus
    satisfy Qt's definition of "rich text" rather than plaintext.

    Specifically:

    * If the :func:`Qt.mightBeRichText` function is available, this tester
      defers to that function.
    * Else, this tester falls back to the :func:`mls.is_ml` function.
    """
    mightBeRichText = getattr(Qt, 'mightBeRichText', None)
    if mightBeRichText:
        return mightBeRichText(text)
    else:
        return mls.is_ml(text)


def decode_qbytearray_ascii(qbytearray: QByteArray) -> str:
    """
    Decode the passed ASCII-encoded Qt-specific byte array into a Python string.
    """
    byte_array = qbytearray.constData() if hasattr(qbytearray, 'constData') else qbytearray.data()
    return str(byte_array, encoding='ascii')