# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_prelink.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sysconfig import PrelinkSysconfig
PRELINK_SYSCONFIG = ("\n# Set this to no to disable prelinking altogether\n# (if you change this from yes to no prelink -ua\n# will be run next night to undo prelinking)\nPRELINKING=no\n\n# Options to pass to prelink\n# -m    Try to conserve virtual memory by allowing overlapping\n#       assigned virtual memory slots for libraries which\n#       never appear together in one binary\n# -R    Randomize virtual memory slot assignments for libraries.\n#       This makes it slightly harder for various buffer overflow\n#       attacks, since library addresses will be different on each\n#       host using -R.\nPRELINK_OPTS=-mR\n\n# How often should full prelink be run (in days)\n# Normally, prelink will be run in quick mode, every\n# $PRELINK_FULL_TIME_INTERVAL days it will be run\n# in normal mode.  Comment it out if it should be run\n# in normal mode always.\nPRELINK_FULL_TIME_INTERVAL=14\n\n# How often should prelink run (in days) even if\n# no packages have been upgraded via rpm.\n# If $PRELINK_FULL_TIME_INTERVAL days have not elapsed\n# yet since last normal mode prelinking, last\n# quick mode prelinking happened less than\n# $PRELINK_NONRPM_CHECK_INTERVAL days ago\n# and no packages have been upgraded by rpm\n# since last quick mode prelinking, prelink\n# will not do anything.\n# Change to\n# PRELINK_NONRPM_CHECK_INTERVAL=0\n# if you want to disable the rpm database timestamp\n# check (especially if you don't use rpm/up2date/yum/apt-rpm\n# exclusively to upgrade system libraries and/or binaries).\nPRELINK_NONRPM_CHECK_INTERVAL=7\n").strip()

def test_sysconfig_prelink():
    result = PrelinkSysconfig(context_wrap(PRELINK_SYSCONFIG))
    assert result['PRELINKING'] == 'no'
    assert result.get('PRELINK_OPTS') == '-mR'
    assert result.get('OPTIONS1') is None
    assert result['PRELINK_NONRPM_CHECK_INTERVAL'] == '7'
    return