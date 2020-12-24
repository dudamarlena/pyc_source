# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_sap.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers.hostname import Hostname as HnF
from insights import SkipComponent
from insights.parsers.lssap import Lssap
from insights.parsers.saphostctrl import SAPHostCtrlInstances
from insights.combiners import sap
from insights.combiners.sap import Sap
from insights.combiners.hostname import Hostname
from insights.tests import context_wrap
import pytest, doctest
Lssap_nw_TEST = ('\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe\n  HA2|  22|       D22|         lu0416|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe\n  HA2|  50|       D50|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D50/exe\n  HA2|  51|       D51|         lu0418|749, patch 10, changelist 1698137|          /usr/sap/HA2/D51/exe\n  HA2|  52|       D52|         lu0418|749, patch 10, changelist 1698137|          /usr/sap/HA2/D52/exe\n==========================================\n').strip()
Lssap_hana_TEST = ('\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       HDB16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/HDB16/exe\n==========================================\n').strip()
Lssap_ascs_TEST = ('\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       ASCS16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/ASCS16/exe\n==========================================\n').strip()
Lssap_all_TEST = ('\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe\n  HA2|  22|       D22|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe\n  HA2|  16|       HDB16|       lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/HDB16/exe\n  HA2|  16|       ASCS16|      lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/ASCS16/exe\n==========================================\n').strip()
Lssap_doc_TEST = ('\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe\n  HA2|  22|       D22|         lu0418|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe\n  HA2|  16|       HDB16|       lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/HDB16/exe\n==========================================\n').strip()
HOSTNAME = 'lu0417.example.com'
HOSTNAME1 = 'li-ld-1810.example.com'
SAPHOSTCTRL_HOSTINSTANCES = '\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D89\n SystemNumber , String , 88\n InstanceName , String , HDB88\n Hostname , String , lu0417\n FullQualifiedHostname , String , lu0417.example.com\n IPAddress , String , 10.0.0.88\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D90\n SystemNumber , String , 90\n InstanceName , String , HDB90\n Hostname , String , lu0418\n FullQualifiedHostname , String , lu0418.example.com\n IPAddress , String , 10.0.0.90\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n'
SAPHOSTCTRL_HOSTINSTANCES_GOOD = '\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D89\n SystemNumber , String , 88\n InstanceName , String , HDB88\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D90\n SystemNumber , String , 90\n InstanceName , String , HDB90\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 08\n InstanceName , String , ERS08\n Hostname , String , d79ers\n FullQualifiedHostname , String , d79ers.example.com\n IPAddress , String , 10.0.0.15\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 07\n InstanceName , String , ASCS07\n Hostname , String , d79ascs\n FullQualifiedHostname , String , d79ascs.example.com\n IPAddress , String , 10.0.0.14\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D79\n SystemNumber , String , 09\n InstanceName , String , DVEBMGS09\n Hostname , String , d79pas\n FullQualifiedHostname , String , d79pas.example.com\n IPAddress , String , 10.0.0.16\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D80\n SystemNumber , String , 10\n InstanceName , String , SCS10\n Hostname , String , d80scs\n FullQualifiedHostname , String , d80scs.example.com\n IPAddress , String , 10.0.0.17\n SapVersionInfo , String , 749, patch 301, changelist 1779613\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D62\n SystemNumber , String , 62\n InstanceName , String , HDB62\n Hostname , String , d62dbsrv\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.1.12\n SapVersionInfo , String , 749, patch 211, changelist 1754007\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D52\n SystemNumber , String , 52\n InstanceName , String , ASCS52\n Hostname , String , d52ascs\n FullQualifiedHostname , String , d52ascs.example.com\n IPAddress , String , 10.0.0.20\n SapVersionInfo , String , 749, patch 401, changelist 1806777\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , D52\n SystemNumber , String , 54\n InstanceName , String , D54\n Hostname , String , d52pas\n FullQualifiedHostname , String , d52pas.example.com\n IPAddress , String , 10.0.0.22\n SapVersionInfo , String , 749, patch 401, changelist 1806777\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , SMA\n SystemNumber , String , 91\n InstanceName , String , SMDA91\n Hostname , String , li-ld-1810\n FullQualifiedHostname , String , li-ld-1810.example.com\n IPAddress , String , 10.0.0.1\n SapVersionInfo , String , 749, patch 200, changelist 1746260\n*********************************************************\n CreationClassName , String , SAPInstance\n SID , String , B15\n SystemNumber , String , 00\n InstanceName , String , HDB00\n Hostname , String , sapb15hdba1\n FullQualifiedHostname , String , li-ld-1810.example.com\n SapVersionInfo , String , 749, patch 418, changelist 1816226\n*********************************************************\n'

def test_lssap_netweaver():
    lssap = Lssap(context_wrap(Lssap_nw_TEST))
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    sap = Sap(hn, None, lssap)
    assert sap['D50'].number == '50'
    assert 'D16' in sap.local_instances
    assert 'D51' in sap.all_instances
    assert 'D51' not in sap.local_instances
    assert sap.is_netweaver is True
    assert sap.is_hana is False
    assert sap.is_ascs is False
    return


def test_saphostcrtl_hana():
    lssap = Lssap(context_wrap(Lssap_nw_TEST))
    inst = SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES))
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    sap = Sap(hn, inst, lssap)
    assert 'D50' not in sap
    assert sap.local_instances == ['HDB88']
    assert 'HDB90' in sap.all_instances
    assert sap['HDB88'].number == '88'
    assert sap['HDB90'].hostname == 'lu0418'
    assert sap['HDB90'].version == '749, patch 211, changelist 1754007'
    assert sap.number('HDB90') == '90'
    assert sap.sid('HDB88') == 'D89'
    assert sap.is_netweaver is False
    assert sap.is_hana is True
    assert sap.is_ascs is False
    return


def test_saphostcrtl_hana_2():
    lssap = Lssap(context_wrap(Lssap_all_TEST))
    inst = SAPHostCtrlInstances(context_wrap(SAPHOSTCTRL_HOSTINSTANCES_GOOD))
    hn = Hostname(HnF(context_wrap(HOSTNAME1)), None, None, None, None)
    sap = Sap(hn, inst, lssap)
    assert 'D50' not in sap
    assert 'HDB00' in sap
    assert sorted(sap.local_instances) == sorted(['HDB88', 'HDB90', 'SMDA91'])
    assert sorted(sap.all_instances) == sorted([
     'ASCS07', 'ASCS52', 'D54', 'DVEBMGS09', 'ERS08', 'HDB00', 'HDB62',
     'HDB88', 'HDB90', 'SCS10', 'SMDA91'])
    assert sorted(sap.business_instances) == sorted([
     'ASCS07', 'ASCS52', 'D54', 'DVEBMGS09', 'ERS08', 'HDB00', 'HDB62',
     'HDB88', 'HDB90', 'SCS10'])
    assert sorted(sap.function_instances) == sorted(['SMDA91'])
    assert sap['HDB88'].number == '88'
    assert sap['HDB90'].hostname == 'li-ld-1810'
    assert sap['DVEBMGS09'].version == '749, patch 301, changelist 1779613'
    assert sap.version('HDB90') == '749, patch 211, changelist 1754007'
    assert sap.hostname('HDB62') == 'd62dbsrv'
    assert sap.type('SCS10') == 'SCS'
    assert sap.is_netweaver is True
    assert sap.is_hana is True
    assert sap.is_ascs is True
    return


def test_lssap_hana():
    lssap = Lssap(context_wrap(Lssap_hana_TEST))
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    sap = Sap(hn, None, lssap)
    assert 'D50' not in sap
    assert sap.is_netweaver is False
    assert sap.is_hana is True
    assert sap.is_ascs is False
    return


def test_lssap_ascs():
    lssap = Lssap(context_wrap(Lssap_ascs_TEST))
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    sap = Sap(hn, None, lssap)
    assert sap['ASCS16'].sid == 'HA2'
    assert sap.is_netweaver is False
    assert sap.is_hana is False
    assert sap.is_ascs is True
    return


def test_all():
    lssap = Lssap(context_wrap(Lssap_all_TEST))
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    sap = Sap(hn, None, lssap)
    assert sap['D16'].version == '749, patch 10, changelist 1698137'
    assert sap['ASCS16'].hostname == 'lu0417'
    assert sap.is_netweaver is True
    assert sap.is_hana is True
    assert sap.is_ascs is True
    return


def test_doc_examples():
    env = {'saps': Sap(Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None), None, Lssap(context_wrap(Lssap_doc_TEST)))}
    failed, total = doctest.testmod(sap, globs=env)
    assert failed == 0
    return


def test_ab():
    hn = Hostname(HnF(context_wrap(HOSTNAME)), None, None, None, None)
    with pytest.raises(SkipComponent) as (se):
        Sap(hn, None, None)
    assert 'No SAP instance.' in str(se)
    return