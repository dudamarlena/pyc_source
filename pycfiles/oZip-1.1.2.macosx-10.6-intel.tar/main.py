# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/main.py
# Compiled at: 2014-08-30 09:16:39
from core.text import TextCompressor
from core.files import FilesCompressor
import os.path, sys

def check_file(path):
    """ Make sure that the file exists """
    if not os.path.exists(path):
        raise ValueError('The path specified does not exists.')


def choose_engine(path):
    """ Choose a compression engine according to the file type """
    ext = path.split('.')
    if ext[(-1)] == 'ozip':
        ext = ext[(-2)]
    else:
        ext = ext[(-1)]
    if ext == 'txt':
        return TextCompressor()
    return FilesCompressor()


def main(path, decompress):
    """ Main function """
    try:
        check_file(path)
    except ValueError as e:
        print str(e)
        sys.exit(1)

    engine = choose_engine(path)
    if decompress:
        try:
            engine.decompress(path)
        except Exception as e:
            return (
             path, str(e))

    else:
        try:
            engine.compress(path)
        except Exception as e:
            return (
             path, str(e))

    return