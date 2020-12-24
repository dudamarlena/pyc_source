# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_whoopsie.py
# Compiled at: 2020-05-07 15:26:17
import doctest, pytest
from insights.parsers import whoopsie
from insights.parsers.whoopsie import Whoopsie
from insights.tests import context_wrap
BOTH_MATCHED = ('\n/var/crash/.reports-1000-user/whoopsie-report\n').strip()
NOT_FIND_MATCHED = ("\n/usr/bin/find: '/var/crash': No such file or directory\n/var/tmp/.reports-1000-user/whoopsie-report\n").strip()
BOTH_NOT_FIND = ("\n/usr/bin/find: '/var/crash': No such file or directory\n/usr/bin/find: '/var/tmp': No such file or directory\n").strip()
BOTH_EMPTY = '\n'
TEST_CASES = [
 (
  BOTH_MATCHED, '1000', '/var/crash/.reports-1000-user/whoopsie-report'),
 (
  NOT_FIND_MATCHED, '1000', '/var/tmp/.reports-1000-user/whoopsie-report'),
 (
  BOTH_NOT_FIND, None, None),
 (
  BOTH_EMPTY, None, None)]

@pytest.mark.parametrize('output, uid, file', TEST_CASES)
def test_whoopsie(output, uid, file):
    test = Whoopsie(context_wrap(output))
    assert test.uid == uid
    assert test.file == file


def test_doc_examples():
    env = {'whoopsie': Whoopsie(context_wrap(BOTH_MATCHED))}
    failed, total = doctest.testmod(whoopsie, globs=env)
    assert failed == 0