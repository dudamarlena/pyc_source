# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/validator.py
# Compiled at: 2018-02-27 19:21:23
# Size of source mod 2**32: 858 bytes
from langdetect import detect_langs
from .models import Comment

class Comment:
    MIN_DETECTION_CONFIDENCE = 0.9

    def __init__(self, comment: Comment, language_code: str='en') -> None:
        self.comment = comment
        self.language_code = language_code
        self.language_code_detected = None

    def is_valid(self) -> bool:
        try:
            self.validate()
        except AssertionError:
            return False
        else:
            return True

    def validate(self) -> None:
        try:
            guess = detect_langs(self.comment.text)[0]
        except IndexError:
            return
        else:
            self.language_code_detected = guess.lang
        assert self.language_code_detected == self.language_code

    def __bool__(self) -> bool:
        return self.is_valid()