# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/enums.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 792 bytes
from __future__ import unicode_literals

class IncrementalSearchDirection(object):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'


class EditingMode(object):
    VI = 'VI'
    EMACS = 'EMACS'


SEARCH_BUFFER = 'SEARCH_BUFFER'
DEFAULT_BUFFER = 'DEFAULT_BUFFER'
SYSTEM_BUFFER = 'SYSTEM_BUFFER'
DUMMY_BUFFER = 'DUMMY_BUFFER'