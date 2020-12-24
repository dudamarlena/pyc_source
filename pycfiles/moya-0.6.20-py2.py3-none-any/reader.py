# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/reader.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals, print_function
from fs.path import join, basename
from fs.errors import FSError
import mimetypes, json

class ReaderError(Exception):
    pass


class UnknownFormat(ReaderError):
    """Attempt to read a format we don't understand"""
    pass


class RelativePathError(ReaderError):
    """Can't read from a relative with without an app"""
    pass


class DataReader(object):
    """Reads and decodes files of known types"""

    def __init__(self, fs):
        self.fs = fs

    def __repr__(self):
        return (b'<reader {!r}>').format(self.fs)

    def read(self, path, app=None, mime_type=None):
        """Read a file"""
        if not path.startswith(b'/'):
            if app is None:
                raise RelativePathError(b"Can't use relative data paths with an application")
            path = join(app.data_directory, path)
        filename = basename(path)
        if mime_type is None:
            mime_type, encoding = mimetypes.guess_type(filename)
        _type, sub_type = mime_type.split(b'/', 1)
        try:
            if mime_type == b'text/plain':
                data = self.fs.gettext(path)
            elif mime_type == b'application/json':
                with self.fs.open(path, b'rt', encoding=b'utf-8') as (f):
                    data = json.load(f)
            elif mime_type == b'application/octet-stream':
                data = self.fs.getbytes(path)
            elif _type == b'text':
                data = self.fs.gettext(path)
            else:
                raise UnknownFormat((b"Moya doesn't know how to read file '{}' (in {!r})").format(path, self.fs))
        except FSError as e:
            from .logic import MoyaException
            info = {b'path': path, 
               b'mime_type': mime_type}
            raise MoyaException(b'data.read-fail', (b'unable to read data from {path} ({e})').format(path=path, e=e), diagnosis=b'check the data exists with **moya fs data --tree /**', info=info)

        return data

    def exists(self, path, app):
        """Check if a file exists"""
        if not path.startswith(b'/'):
            if app is None:
                raise RelativePathError(b"Can't use relative data paths with an application")
            path = join(app.data_directory, path)
        try:
            return self.fs.isfile(path)
        except FSError:
            return False

        return


if __name__ == b'__main__':
    reader = DataReader(None)
    reader.read(b'test.bin')