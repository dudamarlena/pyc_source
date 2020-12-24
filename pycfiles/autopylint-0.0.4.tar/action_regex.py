# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/action_regex.py
# Compiled at: 2018-01-10 14:39:00
"""
Regexes used for pylint rules
"""
import re
STD_IMPORT = re.compile('\n    ^\n    standard\\simport\\s\n    \\"(?P<before>[^"]+)\\"\n    \\sshould\\sbe\\splaced\\sbefore\\s\n    \\"(?P<after>[^"]+)\\"\n    $\n', re.VERBOSE)
FROM_IMP = re.compile('\n    ^\n    from\n    \\s+(?P<library>[\\w\\d_\\.]+)\n    \\s+import\n    \\s+(?P<imports>[\\w\\d_\\.,\\s]+)\n    $\n', re.VERBOSE)
IF_STMT_AND = re.compile('\n    ^\n    if\\s+\n    (?P<first>.*?)\n    \\s+and\\s+\n    (?P<second>.*?):\n    $\n', re.VERBOSE)
IF_STMT_OR = re.compile('\n    ^\n    if\\s+\n    (?P<first>.*?)\n    \\s+or\\s+\n    (?P<second>.*?):\n    $\n', re.VERBOSE)
CONTINUATION = re.compile('\n    ^\n    Wrong\\scontinued\\sindentation\\s\n    \\(\n    (?P<verb>.*?)\n    \\s(?P<count>\\d+)\\s+spaces\n    \\)\n    \\.\n    $\n', re.VERBOSE)
HANGING = re.compile('\n    ^\n    Wrong\\shanging\\sindentation\\s\n    (\n        \\(\n        (?P<verb>.*?)\n        \\s(?P<count>\\d+)\\s+spaces\n        \\)\n    )?\n    \\.\n    $\n', re.VERBOSE)