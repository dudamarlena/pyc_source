# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/unportable.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 428 bytes
import re
PARSE_IMPLICIT_LITERAL_RE = re.compile('(?P<line>(?:\\$?\\{|\\(|\\[|&.+;|[0-9]+|(?:[^!-~]|[A-Z])).*)\\s*')