# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_saphostctrl.py
# Compiled at: 2019-11-14 13:57:46
from ...parsers import saphostctrl, ParseException, SkipException
from ...parsers.saphostctrl import SAPHostCtrlInstances
from ...tests import context_wrap
import doctest, pytest
SAPHOSTCTRL_HOSTINSTANCES_DOCS = '\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D89\n SystemNumber , String , 88\n InstanceName , String , HDB88\n Hostname , String , hdb88\n FullQualifiedHostname , String , hdb88.example.com\n IPAddress , String , 10.0.0.88\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D90\n SystemNumber , String , 90\n InstanceName , String , HDB90\n Hostname , String , hdb90\n FullQualifiedHostname , String , hdb90.example.com\n IPAddress , String , 10.0.0.90\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n'
SAPHOSTCTRL_HOSTINSTANCES_GOOD = '\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D89\n SystemNumber , String , 88\n InstanceName , String , HDB88\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D90\n SystemNumber , String , 90\n InstanceName , String , HDB90\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 08\n InstanceName , String , ERS08\n Hostname , String , d79ers\n FullQualifiedHostname , String , d79ers.example.com\n IPAddress , String , 10.0.0.15\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 07\n InstanceName , String , ASCS07\n Hostname , String , d79ascs\n FullQualifiedHostname , String , d79ascs.example.com\n IPAddress , String , 10.0.0.14\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 09\n InstanceName , String , DVEBMGS09\n Hostname , String , d79pas\n FullQualifiedHostname , String , d79pas.example.com\n IPAddress , String , 10.0.0.16\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D80\n SystemNumber , String , 10\n InstanceName , String , SCS10\n Hostname , String , d80scs\n FullQualifiedHostname , String , d80scs.example.com\n IPAddress , String , 10.0.0.17\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D62\n SystemNumber , String , 62\n InstanceName , String , HDB62\n Hostname , String , d62dbsrv\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.1.12\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D52\n SystemNumber , String , 52\n InstanceName , String , ASCS52\n Hostname , String , d52ascs\n FullQualifiedHostname , String , d52ascs.example.com\n IPAddress , String , 10.0.0.20\n SapVersionInfo , String , 749, patch 401, changelist 1806777\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D52\n SystemNumber , String , 54\n InstanceName , String , D54\n Hostname , String , d52pas\n FullQualifiedHostname , String , d52pas.example.com\n IPAddress , String , 10.0.0.22\n SapVersionInfo , String , 749, patch 401, changelist 1806777\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , SMA\n SystemNumber , String , 91\n InstanceName , String , SMDA91\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 200, changelist 1746260\n'
SAPHOSTCTRL_HOSTINSTANCES_BAD = '\n CreationClassName , String\n SID , String , D89\n SystemNumber , String , 88\n'
SAPHOSTCTRL_HOSTINSTANCES_BAD1 = '\n CreationClassName , String , SAPInstance\n SID , String , D89\n SystemNumber , String , 88\n'

def test_saphostctrl_docs():
    globs = {'sap_inst': SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES_DOCS))}
    failed, total = doctest.testmod(saphostctrl, globs=globs)
    assert failed == 0


def test_saphostctrl():
    sap = SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES_GOOD))
    assert len(sap) == 10
    assert sap.data[(-2)]['SapVersionInfo'] == '749, patch 401, changelist 1806777'
    assert sorted(sap.instances) == sorted([
     'HDB88', 'HDB90', 'ERS08', 'ASCS07', 'DVEBMGS09', 'SCS10', 'HDB62',
     'ASCS52', 'D54', 'SMDA91'])
    for sid in ['D89', 'D90', 'D79', 'D80', 'D62', 'D52', 'SMA']:
        assert sid in sap.sids

    assert sorted(sap.types) == sorted([
     'HDB', 'ERS', 'ASCS', 'DVEBMGS', 'SCS', 'D', 'SMDA'])


def test_saphostctrl_bad():
    with pytest.raises(ParseException) as (pe):
        SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES_BAD))
    assert "Incorrect line: 'CreationClassName , String'" in str(pe)
    with pytest.raises(SkipException) as (pe):
        SAPHostCtrlInstances(context_wrap(''))
    assert 'Empty content' in str(pe)
    with pytest.raises(ParseException) as (pe):
        SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES_BAD1))
    assert 'Missing:' in str(pe)