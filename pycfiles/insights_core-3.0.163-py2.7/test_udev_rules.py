# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_udev_rules.py
# Compiled at: 2020-03-25 13:10:41
import doctest
from insights.parsers import udev_rules
from insights.parsers.udev_rules import UdevRulesFCWWPN
from insights.tests import context_wrap
UDEV_RULES_FILT_HIT = ('\nENV{FC_TARGET_WWPN}!="$*"; GOTO="fc_wwpn_end"\nENV{FC_INITIATOR_WWPN}!="$*"; GOTO="fc_wwpn_end"\nENV{FC_TARGET_LUN}!="$*"; GOTO="fc_wwpn_end"\n').strip()

def test_documentation():
    env = {'udev_rules': UdevRulesFCWWPN(context_wrap(UDEV_RULES_FILT_HIT))}
    failed_count, tests = doctest.testmod(udev_rules, globs=env)
    assert failed_count == 0


def test_udev_rules():
    result = UdevRulesFCWWPN(context_wrap(UDEV_RULES_FILT_HIT))
    for line in ['ENV{FC_TARGET_WWPN}!="$*"; GOTO="fc_wwpn_end"',
     'ENV{FC_INITIATOR_WWPN}!="$*"; GOTO="fc_wwpn_end"',
     'ENV{FC_TARGET_LUN}!="$*"; GOTO="fc_wwpn_end"']:
        assert line in result.lines