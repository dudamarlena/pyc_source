# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wikir/tests/test_docs.py
# Compiled at: 2009-03-26 18:20:42
import wikir, inspect, pydoc
from wikir.tests.shelldoc import find_shell_sessions, validate_session

def test_docs():
    doc = pydoc.splitdoc(inspect.getdoc(wikir))[1]
    for session in find_shell_sessions(doc):
        yield (
         validate_session, session)