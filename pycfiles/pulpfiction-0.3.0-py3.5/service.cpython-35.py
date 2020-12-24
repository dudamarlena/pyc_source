# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tinyfn/service.py
# Compiled at: 2018-02-27 19:30:15
# Size of source mod 2**32: 550 bytes
from typing import List
from .exceptions import LanguageUnsupported
from .parser import Directory as DirectoryParser
from .validator import Comment as Validator

def evaluate(path: str) -> None:
    parser = DirectoryParser(path)
    for _file in parser:
        if not _file.is_supported():
            pass
        else:
            for comment in _file:
                try:
                    validate = Validator(comment)
                    assert bool(validate)
                except AssertionError:
                    raise LanguageUnsupported.from_validator(validate)