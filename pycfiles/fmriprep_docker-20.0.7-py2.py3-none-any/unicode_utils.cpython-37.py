# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/setuptools/setuptools/unicode_utils.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 996 bytes
import unicodedata, sys
from setuptools.extern import six

def decompose(path):
    if isinstance(path, six.text_type):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass

    return path


def filesys_decode(path):
    """
    Ensure that the given path is decoded,
    NONE when no expected encoding works
    """
    if isinstance(path, six.text_type):
        return path
    fs_enc = sys.getfilesystemencoding() or 'utf-8'
    candidates = (fs_enc, 'utf-8')
    for enc in candidates:
        try:
            return path.decode(enc)
        except UnicodeDecodeError:
            continue


def try_encode(string, enc):
    """turn unicode encoding into a functional routine"""
    try:
        return string.encode(enc)
    except UnicodeEncodeError:
        return