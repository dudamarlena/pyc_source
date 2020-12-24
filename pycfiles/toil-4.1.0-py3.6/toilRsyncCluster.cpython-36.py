# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilRsyncCluster.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 1974 bytes
"""
Rsyncs into the toil appliance container running on the leader of the cluster
"""
import argparse, logging
from toil.lib.bioio import parseBasicOptions, getBasicOptionParser
from toil.provisioners import clusterFactory
from toil.utils import addBasicProvisionerOptions
logger = logging.getLogger(__name__)

def main():
    parser = getBasicOptionParser()
    parser = addBasicProvisionerOptions(parser)
    parser.add_argument('--insecure', dest='insecure', action='store_true', required=False, help='Temporarily disable strict host key checking.')
    parser.add_argument('args', nargs=(argparse.REMAINDER), help='Arguments to pass to`rsync`. Takes any arguments that rsync accepts. Specify the remote with a colon. For example, to upload `example.py`, specify `toil rsync-cluster -p aws test-cluster example.py :`.\nOr, to download a file from the remote:, `toil rsync-cluster -p aws test-cluster :example.py .`')
    config = parseBasicOptions(parser)
    cluster = clusterFactory(provisioner=(config.provisioner), clusterName=(config.clusterName),
      zone=(config.zone))
    cluster.getLeader().coreRsync(args=(config.args), strict=(not config.insecure))