# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sapcontrol.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import sapcontrol, SkipException, ParseException
from insights.parsers.sapcontrol import SAPControlSystemUpdateList
from insights.tests import context_wrap
import pytest, doctest
RKS_STATUS = ('\n29.01.2019 01:20:36\nGetSystemUpdateList\nOK\nhostname, instanceNr, status, starttime, endtime, dispstatus\nvm37-39, 00, Running, 29.01.2019 00:00:02, 29.01.2019 01:10:11, GREEN\nvm37-39, 02, Running, 29.01.2019 00:00:05, 29.01.2019 01:11:11, GREEN\nvm37-39, 03, Running, 29.01.2019 00:00:05, 29.01.2019 01:12:36, GREEN\n').strip()
RKS_STATUS_AB1 = ('\n').strip()
RKS_STATUS_AB2 = ('\n29.01.2019 01:20:26\nGetSystemUpdateList\nFAIL: NIECONN_REFUSED (Connection refused), NiRawConnect failed in plugin_fopen()\n').strip()
RKS_STATUS_AB3 = ('\n29.01.2019 01:20:36\nGetSystemUpdateList\nOK\nhostname, instanceNr, status, starttime, endtime, dispstatus\n').strip()

def test_sapcontrol_rks_abnormal():
    with pytest.raises(SkipException):
        SAPControlSystemUpdateList(context_wrap(RKS_STATUS_AB1))
    with pytest.raises(ParseException):
        SAPControlSystemUpdateList(context_wrap(RKS_STATUS_AB2))
    with pytest.raises(SkipException):
        SAPControlSystemUpdateList(context_wrap(RKS_STATUS_AB3))


def test_sapcontrol_status():
    rks = SAPControlSystemUpdateList(context_wrap(RKS_STATUS))
    assert rks.is_running
    assert rks.is_green
    assert rks.data[0]['status'] == 'Running'
    assert rks.data[1]['instanceNr'] == '02'
    assert rks.data[(-1)]['dispstatus'] == 'GREEN'


def test_doc_examples():
    env = {'rks': SAPControlSystemUpdateList(context_wrap(RKS_STATUS))}
    failed, total = doctest.testmod(sapcontrol, globs=env)
    assert failed == 0