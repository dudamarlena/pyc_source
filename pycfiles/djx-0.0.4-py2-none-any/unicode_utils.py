# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/unicode_utils.py
# Compiled at: 2019-02-06 16:42:30
import unicodedata, sys, re
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

    return


CODING_RE = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)')

def detect_encoding(fp):
    first_line = fp.readline()
    fp.seek(0)
    m = CODING_RE.match(first_line)
    if m is None:
        return
    else:
        return m.group(1).decode('ascii')