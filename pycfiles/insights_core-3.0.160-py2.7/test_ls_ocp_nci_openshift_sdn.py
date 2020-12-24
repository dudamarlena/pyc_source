# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_ocp_nci_openshift_sdn.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_ocp_cni_openshift_sdn
from insights.parsers.ls_ocp_cni_openshift_sdn import LsOcpCniOpenshiftSdn
from insights.tests import context_wrap
LS_CNI_OPENSHIFT_SDN = ('\ntotal 52\n-rw-r--r--. 1 root root 64 Aug  5 23:26 10.130.0.102\n-rw-r--r--. 1 root root 64 Aug  5 23:26 10.130.0.103\n-rw-r--r--. 1 root root 64 Aug  6 22:52 10.130.0.116\n-rw-r--r--. 1 root root 64 Aug  6 22:52 10.130.0.117\n-rw-r--r--. 1 root root 64 Aug  5 06:59 10.130.0.15\n-rw-r--r--. 1 root root 64 Aug  5 07:02 10.130.0.20\n-rw-r--r--. 1 root root 12 Aug  6 22:52 last_reserved_ip.0\n').strip()

def test_ls_ocp_cni_openshift_sdn():
    ls_ocp_cni_openshift_sdn = LsOcpCniOpenshiftSdn(context_wrap(LS_CNI_OPENSHIFT_SDN, path='insights_commands/ls_-l_.var.lib.cni.networks.openshift-sdn'))
    assert len(ls_ocp_cni_openshift_sdn.files_of('/var/lib/cni/networks/openshift-sdn')) == 7
    assert ls_ocp_cni_openshift_sdn.files_of('/var/lib/cni/networks/openshift-sdn') == ['10.130.0.102', '10.130.0.103',
     '10.130.0.116', '10.130.0.117',
     '10.130.0.15', '10.130.0.20',
     'last_reserved_ip.0']


def test_ls_ocp_cni_openshift_sdn_doc_examples():
    env = {'ls_ocp_cni_openshift_sdn': LsOcpCniOpenshiftSdn(context_wrap(LS_CNI_OPENSHIFT_SDN, path='insights_commands/ls_-l_.var.lib.cni.networks.openshift-sdn'))}
    failed, total = doctest.testmod(ls_ocp_cni_openshift_sdn, globs=env)
    assert failed == 0