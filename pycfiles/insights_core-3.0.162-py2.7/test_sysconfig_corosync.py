# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_corosync.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import CorosyncSysconfig
from insights.tests import context_wrap
corosync_content = '\n# Corosync init script configuration file\n\n# COROSYNC_INIT_TIMEOUT specifies number of seconds to wait for corosync\n# initialization (default is one minute).\nCOROSYNC_INIT_TIMEOUT=60\n\n# COROSYNC_OPTIONS specifies options passed to corosync command\n# (default is no options).\n# See "man corosync" for detailed descriptions of the options.\nCOROSYNC_OPTIONS=""\n'

def test_corosync_sysconfig():
    result = CorosyncSysconfig(context_wrap(corosync_content))
    assert result.data['COROSYNC_OPTIONS'] == ''
    assert result.data['COROSYNC_INIT_TIMEOUT'] == '60'
    assert result.options == ''
    assert result.unparsed_lines == []