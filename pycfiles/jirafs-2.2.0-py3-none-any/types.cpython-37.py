# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/types.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 146 bytes
from typing import Dict, Union
JirafsMacroAttributeValue = Union[(str, float, bool)]
JirafsMacroAttributes = Dict[(str, JirafsMacroAttributeValue)]