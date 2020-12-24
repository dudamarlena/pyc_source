# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/unportable.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 428 bytes
import re
PARSE_IMPLICIT_LITERAL_RE = re.compile('(?P<line>(?:\\$?\\{|\\(|\\[|&.+;|[0-9]+|(?:[^!-~]|[A-Z])).*)\\s*')