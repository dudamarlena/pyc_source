# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rdma_config.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.tests import context_wrap
from insights.parsers import rdma_config as scc, SkipException
RDMA_CONFIG = "\n# Load IPoIB\nIPOIB_LOAD=yes\n# Load SRP (SCSI Remote Protocol initiator support) module\nSRP_LOAD=yes\n# Load SRPT (SCSI Remote Protocol target support) module\nSRPT_LOAD=yes\n# Load iSER (iSCSI over RDMA initiator support) module\nISER_LOAD=yes\n# Load iSERT (iSCSI over RDMA target support) module\nISERT_LOAD=yes\n# Load RDS (Reliable Datagram Service) network protocol\nRDS_LOAD=no\n# Load NFSoRDMA client transport module\nXPRTRDMA_LOAD=yes\n# Load NFSoRDMA server transport module\nSVCRDMA_LOAD=no\n# Load Tech Preview device driver modules\nTECH_PREVIEW_LOAD=no\n# Should we modify the system mtrr registers?  We may need to do this if you\n# get messages from the ib_ipath driver saying that it couldn't enable\n# write combining for the PIO buffs on the card.\n#\n# Note: recent kernels should do this for us, but in case they don't, we'll\n# leave this option\nFIXUP_MTRR_REGS=no\n"
RDMA_CONFIG_INPUT_EMPTY = "\n# Load IPoIB\n#IPOIB_LOAD=yes\n# Load SRP (SCSI Remote Protocol initiator support) module\n#SRP_LOAD=yes\n# Load SRPT (SCSI Remote Protocol target support) module\n#SRPT_LOAD=yes\n# Load iSER (iSCSI over RDMA initiator support) module\n#ISER_LOAD=yes\n# Load iSERT (iSCSI over RDMA target support) module\n#ISERT_LOAD=yes\n# Load RDS (Reliable Datagram Service) network protocol\n#RDS_LOAD=no\n# Load NFSoRDMA client transport module\n#XPRTRDMA_LOAD=yes\n# Load NFSoRDMA server transport module\n#SVCRDMA_LOAD=no\n# Load Tech Preview device driver modules\n#TECH_PREVIEW_LOAD=no\n# Should we modify the system mtrr registers?  We may need to do this if you\n# get messages from the ib_ipath driver saying that it couldn't enable\n# write combining for the PIO buffs on the card.\n#\n# Note: recent kernels should do this for us, but in case they don't, we'll\n# leave this option\n#FIXUP_MTRR_REGS=no\n"

def test_rdma_config():
    rdma_config = scc.RdmaConfig(context_wrap(RDMA_CONFIG))
    assert rdma_config['IPOIB_LOAD'] == 'yes'
    assert rdma_config['SRP_LOAD'] == 'yes'
    assert rdma_config['SVCRDMA_LOAD'] == 'no'


def test_rdma_config_empty():
    with pytest.raises(SkipException):
        scc.RdmaConfig(context_wrap(RDMA_CONFIG_INPUT_EMPTY))


def test_rdma_config_doc():
    env = {'rdma_conf': scc.RdmaConfig(context_wrap(RDMA_CONFIG))}
    failed, total = doctest.testmod(scc, globs=env)
    assert failed == 0