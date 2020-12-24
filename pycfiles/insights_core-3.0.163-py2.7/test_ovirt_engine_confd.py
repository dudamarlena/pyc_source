# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ovirt_engine_confd.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ovirt_engine_confd import OvirtEngineConfd
from insights.tests import context_wrap
CONFD_MATCH = ('\nJBOSS_HOME="/usr/share/jbossas"\nENGINE_PKI="/etc/pki/ovirt-engine"\nENGINE_PKI_CA="/etc/pki/ovirt-engine/ca.pem"\nENGINE_PKI_ENGINE_CERT="/etc/pki/ovirt-engine/certs/engine.cer"\nENGINE_TMP="${ENGINE_VAR}/tmp"\n').strip()
CONFD_NOT_MATCH = ('\nJBOSS_HOME="/usr/share/jbossas"\nENGINE_PKI="/etc/pki/ovirt-engine"\nENGINE_PKI_CA="/etc/pki/ovirt-engine/ca.pem"\nENGINE_PKI_ENGINE_CERT="/etc/pki/ovirt-engine/certs/engine.cer"\n').strip()

def test_ovirt_engine_confd():
    match_result = OvirtEngineConfd(context_wrap(CONFD_MATCH))
    assert 'tmp' in match_result.get('ENGINE_TMP')
    no_match_result = OvirtEngineConfd(context_wrap(CONFD_NOT_MATCH))
    assert no_match_result.get('ENGINE_TMP') is None
    return