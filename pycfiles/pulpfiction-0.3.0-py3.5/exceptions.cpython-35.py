# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/exceptions.py
# Compiled at: 2018-02-27 19:20:18
# Size of source mod 2**32: 554 bytes
from .validator import Comment as CommentValidator

class LanguageUnsupported(BaseException):

    @classmethod
    def from_validator(cls, validator: CommentValidator):
        msg = 'Comment "{text}" detected to be not in \'{language_code}\':at: {path}:{line_num}'.format(text=validator.comment.text, language_code=validator.language_code, path=validator.comment.filepath, line_num=validator.comment.line_num)
        return cls(msg)