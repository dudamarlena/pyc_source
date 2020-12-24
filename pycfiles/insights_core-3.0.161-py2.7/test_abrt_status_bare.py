# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_abrt_status_bare.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import abrt_status_bare
from insights.parsers.abrt_status_bare import AbrtStatusBare
from insights.tests import context_wrap
import doctest
OUTPUT = ('\n420\n').strip()
OUTPUT_MULTILINE = ('\n1997\nThis line will never exist in real output, but it is ignored.\n').strip()

def test():
    result = AbrtStatusBare(context_wrap(OUTPUT))
    assert result.problem_count == 420
    result = AbrtStatusBare(context_wrap(OUTPUT_MULTILINE))
    assert result.problem_count == 1997


def test_docs():
    env = {'abrt_status_bare': AbrtStatusBare(context_wrap(OUTPUT_MULTILINE)), 
       'AbrtStatusBare': AbrtStatusBare}
    failed, total = doctest.testmod(abrt_status_bare, globs=env)
    assert failed == 0