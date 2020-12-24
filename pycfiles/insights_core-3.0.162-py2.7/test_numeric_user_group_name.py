# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_numeric_user_group_name.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.numeric_user_group_name import NumericUserGroupName
from insights.tests import context_wrap
from insights.parsers import ParseException
from insights.core.plugins import ContentException
ZERO = ('\n/etc/passwd:0\n/etc/group:0\n').strip()
NONZERO_1 = ('\n/etc/passwd:3\n/etc/group:0\n').strip()
NONZERO_2 = ('\n/etc/passwd:0\n/etc/group:4\n').strip()
NONZERO_3 = ('\n/etc/passwd:1\n/etc/group:1\n').strip()
UNSTRIPPED_ZERO = '\n\n/etc/passwd:0\n/etc/group:0\n\n'
UNSTRIPPED_NONZERO_1 = '\n\n/etc/passwd:3\n/etc/group:0\n\n'
UNSTRIPPED_NONZERO_2 = '\n\n/etc/passwd:0\n/etc/group:4\n\n'
UNSTRIPPED_NONZERO_3 = '\n\n/etc/passwd:1\n/etc/group:1\n\n'
ERRORS_1 = '\n\n/etc/passwd:1\n/bin/grep: /etc/group: No such file or directory\n\n'
ERRORS_2 = '\n\n/bin/grep: /etc/passwd: No such file or directory\n/etc/group:1\n\n'
ERRORS_3 = '\n\n/bin/grep: /etc/passwd: No such file or directory\n/etc/group:0\n\n'
ERRORS_4 = '\n\n/bin/grep: /etc/passwd: No such file or directory\n/bin/grep: /etc/group: No such file or directory\n\n'
ERRORS_5 = '\n\n/bin/grep: No such file or directory\n\n'
ERRORS_6 = '\n\n/etc/passwd: d:\n/etc/group: No such file or directory\n/bin/group:7\n/bin/etc/group:7\n/bin/grep: No such file or directory\n# should be ignored:\n/etc/passwd:0\n# valid output for /etc/passwd on the following line:\n/etc/passwd:1\n/bin/group:4\n/bin/gry\n# should be ignored\n/etc/group:0\n# valid output for /etc/group on the following line:\n/etc/group:1\n/bin/grep: /etc/passwd:3\n'

def test_numeric_user_group_name_1():
    for data in [ZERO, UNSTRIPPED_ZERO]:
        numeric_user_group_name = NumericUserGroupName(context_wrap(data))
        assert not numeric_user_group_name.has_numeric_user_or_group


def test_numeric_user_group_name_2():
    for data in [NONZERO_1, NONZERO_2, NONZERO_3, UNSTRIPPED_NONZERO_1, UNSTRIPPED_NONZERO_2,
     UNSTRIPPED_NONZERO_3, ERRORS_6]:
        numeric_user_group_name = NumericUserGroupName(context_wrap(data))
        assert numeric_user_group_name.has_numeric_user_or_group


def test_numeric_user_group_name_6():
    for data in [NONZERO_1, UNSTRIPPED_NONZERO_1]:
        numeric_user_group_name = NumericUserGroupName(context_wrap(data))
        assert numeric_user_group_name.nr_numeric_user == 3
        assert numeric_user_group_name.nr_numeric_group == 0


def test_numeric_user_group_name_7():
    for data in [NONZERO_2, UNSTRIPPED_NONZERO_2]:
        numeric_user_group_name = NumericUserGroupName(context_wrap(data))
        assert numeric_user_group_name.nr_numeric_user == 0
        assert numeric_user_group_name.nr_numeric_group == 4


def test_numeric_user_group_name_8():
    for data in [NONZERO_3, UNSTRIPPED_NONZERO_3, ERRORS_6]:
        numeric_user_group_name = NumericUserGroupName(context_wrap(data))
        assert numeric_user_group_name.nr_numeric_user == 1
        assert numeric_user_group_name.nr_numeric_group == 1


def test_numeric_user_group_name_9():
    for data in [ERRORS_1, ERRORS_2, ERRORS_3, ERRORS_4]:
        try:
            NumericUserGroupName(context_wrap(data))
            assert False
        except ParseException:
            assert True


def test_numeric_user_group_name_10():
    try:
        NumericUserGroupName(context_wrap(ERRORS_5))
        assert False
    except ContentException:
        assert True