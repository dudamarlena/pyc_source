# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilSshCluster.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 1812 bytes
"""
SSHs into the toil appliance container running on the leader of the cluster
"""
import argparse, logging, sys
from toil.provisioners import clusterFactory
from toil.lib.bioio import parseBasicOptions, getBasicOptionParser
from toil.utils import addBasicProvisionerOptions
logger = logging.getLogger(__name__)

def main():
    parser = getBasicOptionParser()
    parser = addBasicProvisionerOptions(parser)
    parser.add_argument('--insecure', action='store_true', help='Temporarily disable strict host key checking.')
    parser.add_argument('--sshOption', dest='sshOptions', default=[], action='append', help='Pass an additional option to the SSH command.')
    parser.add_argument('args', nargs=(argparse.REMAINDER))
    config = parseBasicOptions(parser)
    cluster = clusterFactory(provisioner=(config.provisioner), clusterName=(config.clusterName),
      zone=(config.zone))
    command = config.args if config.args else ['bash']
    (cluster.getLeader().sshAppliance)(*command, strict=not config.insecure, tty=sys.stdin.isatty(), sshOptions=config.sshOptions)