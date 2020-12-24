# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/parser.py
# Compiled at: 2018-02-27 18:34:15
# Size of source mod 2**32: 1852 bytes
import io, os
from typing import Iterable
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token
import pygments.util
from .models import Comment, File

class Directory:

    def __init__(self, path: str) -> None:
        self.path = path

    def filepaths(self, path=None) -> Iterable[File]:
        """Yields File recursively from this directory."""
        if not path:
            path = self.path
        for dirpath, dirs, files in os.walk(path):
            for name in files:
                filename = os.path.join(dirpath, name)
                yield File(os.path.abspath(filename))
                if not dirs:
                    continue
                else:
                    for d in dirs:
                        self.filepaths(os.path.join(dirpath, d))

    def __iter__(self) -> Iterable[File]:
        return self.filepaths()


class File:

    def __init__(self, path: str) -> None:
        self.path = path
        try:
            self.lexer = get_lexer_for_filename(path)
        except pygments.util.ClassNotFound:
            self.lexer = None

    def comments(self, path=None) -> Iterable[Comment]:
        """Yields Comments in this file."""
        if not self.lexer:
            return
        with io.open(self.path, 'r', encoding='utf8') as (f):
            try:
                for idx, Class, value in self.lexer.get_tokens_unprocessed(f.read()):
                    if Class in (
                     Token.Comment.Multiline,
                     Token.Comment.Single):
                        yield Comment(self.path, value, idx)

            except UnicodeDecodeError:
                pass

    def __iter__(self) -> Iterable[Comment]:
        return self.comments()