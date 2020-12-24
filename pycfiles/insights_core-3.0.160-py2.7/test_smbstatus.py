# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_smbstatus.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import smbstatus
from insights.parsers.smbstatus import SmbstatusS, Smbstatusp, Statuslist
from insights.tests import context_wrap
from insights.parsers import ParseException, SkipException
import pytest, doctest
SMBSTATUSS = '\n\nService      pid     Machine       Connected at                     Encryption   Signing\n---------------------------------------------------------------------------------------------\nshare_test1  12668   10.66.208.149 Wed Sep 27 10:33:55 AM 2017 CST  -            -\nshare_test2  12648   10.66.208.159 Wed Sep 27 11:33:55 AM 2017 CST  -            -\nshare_test3  13628   10.66.208.169 Wed Sep 27 12:33:55 AM 2017 CST  -            -\n\n'
SMBSTATUSP = '\n\nSamba version 4.6.2\nPID     Username     Group        Machine                                   Protocol Version  Encryption           Signing\n----------------------------------------------------------------------------------------------------------------------------------------\n12668   testsmb       zjjsmb       10.66.208.149 (ipv4:10.66.208.149:44376)  SMB2_02           -                    -\n12648   test2smb      test2smb     10.66.208.159 (ipv4:10.66.208.159:24376)  SMB2_02           -                    -\n13628   test3smb      test3smb     10.66.208.169 (ipv4:10.66.208.169:34376)  SMB2_02           -                    -\n'
SMBSTATUSS_EXP = '\n\nxService      pid     Machine       Connected at                     Encryption   Signing\n---------------------------------------------------------------------------------------------\nshare_test1  12668   10.66.208.149 Wed Sep 27 10:33:55 AM 2017 CST  -            -\nshare_test2  12648   10.66.208.159 Wed Sep 27 11:33:55 AM 2017 CST  -            -\nshare_test3  13628   10.66.208.169 Wed Sep 27 12:33:55 AM 2017 CST  -            -\n\n'
SMBSTATUSP_EXP1 = "\nCan't open sessionid.tdb\n"
SMBSTATUSP_EXP2 = '\n'
SMBSTATUSP_DOC = '\nSamba version 4.6.2\nPID     Username     Group        Machine                                   Protocol Version  Encryption           Signing\n--------------------------------------------------------------------------------------------------------------------------\n12668   testsmb       testsmb       10.66.208.149 (ipv4:10.66.208.149:44376)  SMB2_02           -                    -\n'
SMBSTATUSS_DOC = '\nService      pid     Machine       Connected at                     Encryption   Signing\n----------------------------------------------------------------------------------------\nshare_test   13668   10.66.208.149 Wed Sep 27 10:33:55 AM 2017 CST  -            -\n'

def test_smbstatuss():
    smbstatuss = SmbstatusS(context_wrap(SMBSTATUSS))
    assert smbstatuss.data[2]['pid'] == '13628'
    assert smbstatuss.data[1]['Connected_at'] == 'Wed Sep 27 11:33:55 AM 2017 CST'
    assert smbstatuss.data[1]['Encryption'] == '-'
    for result in smbstatuss:
        if result['Service'] == 'share_test1':
            assert result['pid'] == '12668'


def test_smbstatusp():
    smbstatusp = Smbstatusp(context_wrap(SMBSTATUSP))
    assert smbstatusp.data[2]['Username'] == 'test3smb'
    assert smbstatusp.data[1]['Protocol_Version'] == 'SMB2_02'
    assert smbstatusp.data[1]['Signing'] == '-'
    for result in smbstatusp:
        if result['PID'] == '12668':
            assert result['Username'] == 'testsmb'


def test_statuslist_empty_exp():
    with pytest.raises(SkipException) as (pe):
        Statuslist(context_wrap(''))
        assert 'Empty content.' in str(pe)


def test_statuslist_exp():
    with pytest.raises(ParseException) as (pe):
        Statuslist(context_wrap("Can't open sessionid.tdb"))
        assert "Can't open sessionid.tdb" in str(pe)


def test_smbstatusS_exp():
    with pytest.raises(ParseException) as (pe):
        SmbstatusS(context_wrap(SMBSTATUSS_EXP))
        assert 'Cannot find the header line.' in str(pe)


def test_smbstatusp_exp():
    with pytest.raises(ParseException) as (pe):
        Smbstatusp(context_wrap(SMBSTATUSP_EXP1))
        assert 'Cannot find the header line.' in str(pe)
    with pytest.raises(SkipException) as (pe):
        Smbstatusp(context_wrap(SMBSTATUSP_EXP2))
        assert 'Empty content.' in str(pe)


def test_smbstatus_doc():
    env = {'SmbstatusS': SmbstatusS, 
       'smbstatuss_info': SmbstatusS(context_wrap(SMBSTATUSS_DOC)), 
       'Smbstatusp': Smbstatusp, 
       'smbstatusp_info': Smbstatusp(context_wrap(SMBSTATUSP_DOC))}
    failed, total = doctest.testmod(smbstatus, globs=env)
    assert failed == 0