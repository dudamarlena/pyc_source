# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sap_host_profile.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import sap_host_profile, SkipException
from insights.parsers.sap_host_profile import SAPHostProfile
from insights.tests import context_wrap
import doctest, pytest
HOST_PROFILE_DOC = ('\nSAPSYSTEMNAME = SAP\nSAPSYSTEM = 99\nservice/porttypes = SAPHostControl SAPOscol SAPCCMS\nDIR_LIBRARY =\nDIR_EXECUTABLE = /usr/sap/hostctrl/exe\nDIR_PROFILE = /usr/sap/hostctrl/exe\nDIR_GLOBAL = /usr/sap/hostctrl/exe\nDIR_INSTANCE = /usr/sap/hostctrl/exe\nDIR_HOME = /usr/sap/hostctrl/work\n').strip()
HOST_PROFILE_AB = ('\nSAPSYSTEMNAME = SAP\nSAPSYSTEM = 99\nservice/porttypes = SAPHostControl SAPOscol SAPCCMS\nDIR_LIBRARY = /usr/sap/hostctrl/exe\nDIR_EXECUTABLE = /usr/sap/hostctrl/exe\nDIR_PROFILE = /usr/sap/hostctrl/exe\nDIR_GLOBAL\n').strip()

def test_sap_host_profile():
    hpf = SAPHostProfile(context_wrap(HOST_PROFILE_DOC))
    assert 'SAPSYSTEM' in hpf
    assert hpf['DIR_GLOBAL'] == '/usr/sap/hostctrl/exe'
    assert hpf['DIR_LIBRARY'] == ''


def test_sap_host_profile_abnormal():
    with pytest.raises(SkipException) as (s):
        SAPHostProfile(context_wrap(HOST_PROFILE_AB))
    assert "Incorrect line: 'DIR_GLOBAL'" in str(s)


def test_doc_examples():
    env = {'hpf': SAPHostProfile(context_wrap(HOST_PROFILE_DOC))}
    failed, total = doctest.testmod(sap_host_profile, globs=env)
    assert failed == 0