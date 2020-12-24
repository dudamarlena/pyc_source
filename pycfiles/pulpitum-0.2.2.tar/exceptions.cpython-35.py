# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/exceptions.py
# Compiled at: 2018-02-27 19:20:18
# Size of source mod 2**32: 554 bytes
from .validator import Comment as CommentValidator

class LanguageUnsupported(BaseException):

    @classmethod
    def from_validator(cls, validator: CommentValidator):
        msg = 'Comment "{text}" detected to be not in \'{language_code}\':at: {path}:{line_num}'.format(text=validator.comment.text, language_code=validator.language_code, path=validator.comment.filepath, line_num=validator.comment.line_num)
        return cls(msg)