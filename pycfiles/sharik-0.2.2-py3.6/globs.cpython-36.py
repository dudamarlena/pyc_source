# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sharik/globs.py
# Compiled at: 2019-12-14 09:29:54
# Size of source mod 2**32: 633 bytes
from re import compile
from fnmatch import translate
from typing import Iterable, Optional, Pattern
_START = '(^|[/\\\\])'
_END = '([/\\\\]|$)'

def globs_to_pattern(glob_patterns: Iterable[str]) -> Optional[Pattern]:
    if len(glob_patterns) == 0:
        return
    else:
        return compile(_START + '|'.join(f"({translate(glob_pattern)})" for glob_pattern in glob_patterns) + _END)