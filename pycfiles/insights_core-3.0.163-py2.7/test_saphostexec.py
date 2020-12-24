# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_saphostexec.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import saphostexec, SkipException
from insights.parsers.saphostexec import SAPHostExecStatus, SAPHostExecVersion
from insights.tests import context_wrap
import pytest, doctest
STATUS_DOC = ('\nsaphostexec running (pid = 9159)\nsapstartsrv running (pid = 9163)\nsaposcol running (pid = 9323)\n').strip()
STATUS_ABNORMAL = ('\nsaphostexec running (pid = 9159)\nsapstartsrv run (pid = 9163)\nsaposcol (pid = 9323)\n').strip()
VER_DOC = ('\n*************************** Component ********************\n/usr/sap/hostctrl/exe/saphostexec: 721, patch 1011, changelist 1814854, linuxx86_64, opt (Jan 13 2018, 04:43:56)\n/usr/sap/hostctrl/exe/sapstartsrv: 721, patch 1011, changelist 1814854, linuxx86_64, opt (Jan 13 2018, 04:43:56)\n/usr/sap/hostctrl/exe/saphostctrl: 721, patch 1011, changelist 1814854, linuxx86_64, opt (Jan 13 2018, 04:43:56)\n/usr/sap/hostctrl/exe/xml71d.so: 721, patch 1011, changelist 1814854, linuxx86_64, opt (Jan 13 2018, 01:12:10)\n**********************************************************\n--------------------\nSAPHOSTAGENT information\n--------------------\nkernel release                721\nkernel make variant           721_REL\ncompiled on                   Linux GNU SLES-9 x86_64 cc4.1.2  for linuxx86_64\ncompiled for                  64 BIT\ncompilation mode              Non-Unicode\ncompile time                  Jan 13 2018 04:40:52\npatch number                  33\nlatest change number          1814854\n---------------------\nsupported environment\n---------------------\noperating system\nLinux 2.6\nLinux 3\nLinux\n').strip()
SHA_STOP = ('\nsaphostexec stopped\n').strip()

def test_saphostexec_status_abnormal():
    with pytest.raises(SkipException) as (s):
        SAPHostExecStatus(context_wrap(STATUS_ABNORMAL))
    assert "Incorrect status: 'sapstartsrv run (pid = 9163)'" in str(s)
    assert "Incorrect status: 'saposcol (pid = 9,23)'" not in str(s)


def test_saphostexec_status():
    sha_status = SAPHostExecStatus(context_wrap(STATUS_DOC))
    assert sha_status.is_running is True
    assert sha_status.services['saphostexec'] == '9159'
    assert 'saposcol' in sha_status
    sha_status = SAPHostExecStatus(context_wrap(SHA_STOP))
    assert sha_status.is_running is False
    assert sha_status.services == {}
    assert 'saposcol' not in sha_status


def test_saphostexec_version():
    sha_ver = SAPHostExecVersion(context_wrap(VER_DOC))
    assert sha_ver.components['saphostexec'].version == '721'
    assert sha_ver.components['saphostexec'].patch == '1011'
    assert sha_ver.components['xml71d.so'].changelist == '1814854'
    assert 'abc' not in sha_ver


def test_doc_examples():
    env = {'sha_status': SAPHostExecStatus(context_wrap(STATUS_DOC)), 
       'sha_version': SAPHostExecVersion(context_wrap(VER_DOC))}
    failed, total = doctest.testmod(saphostexec, globs=env)
    assert failed == 0