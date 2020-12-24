# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bruc5529/git/fleece/fleece/utils.py
# Compiled at: 2019-11-06 12:49:13
import re, sys

def _fullmatch(pattern, text, *args, **kwargs):
    """re.fullmatch is not available on Python<3.4."""
    match = re.match(pattern, text, *args, **kwargs)
    if match.group(0) == text:
        return match
    else:
        return


if sys.version_info >= (3, 4):
    fullmatch = re.fullmatch
else:
    fullmatch = _fullmatch