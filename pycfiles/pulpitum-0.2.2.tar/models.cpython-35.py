# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/models.py
# Compiled at: 2018-02-27 19:29:17
# Size of source mod 2**32: 532 bytes
import os

class Comment:

    def __init__(self, filepath: str, text: str, line_num: int) -> None:
        self.filepath = filepath
        self.text = text
        self.line_num = line_num


class File:

    def __init__(self, path: str) -> None:
        self.path = path

    def is_supported(self) -> bool:
        filename, ext = os.path.splitext(self.path)
        return ext[1:] in FileExtension.SUPPORTED


class FileExtension:
    SUPPORTED = [
     'go',
     'js',
     'php',
     'py',
     'rb']