# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cron_daily_rhsmd.py
# Compiled at: 2020-04-23 14:49:03
import doctest
from insights.parsers import cron_daily_rhsmd
from insights.parsers.cron_daily_rhsmd import CronDailyRhsmd
from insights.tests import context_wrap
RHSMD_1 = ('\nconfig=$(grep -E "^processTimeout" /etc/rhsm/rhsm.conf | grep -Po "[0-9]+")\nrhsmd_timeout=$config\nabc=$config\n').strip()

def test_docs():
    CronDailyRhsmd.collect('config_lines', lambda n: n if '$config' in n else '')
    CronDailyRhsmd.any('one_config_line', lambda n: n if '$config' in n else '')
    env = {'rhsmd': CronDailyRhsmd(context_wrap(RHSMD_1))}
    failed, total = doctest.testmod(cron_daily_rhsmd, globs=env)
    assert failed == 0


def test_parser():
    cron_daily_rhsmd.CronDailyRhsmd.collect('config_varialbe_lines', lambda n: n if '$config' in n else '')
    cron_daily_rhsmd.CronDailyRhsmd.any('rhsmd_timeout', lambda n: n if 'rhsmd_timeout' in n else '')
    rhs = cron_daily_rhsmd.CronDailyRhsmd(context_wrap(RHSMD_1))
    assert rhs.rhsmd_timeout == 'rhsmd_timeout=$config'
    assert rhs.config_varialbe_lines == ['rhsmd_timeout=$config', 'abc=$config']