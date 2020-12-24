# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilDestroyCluster.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 1161 bytes
"""
Terminates the specified cluster and associated resources
"""
from toil.provisioners import clusterFactory
from toil.lib.bioio import parseBasicOptions, getBasicOptionParser
from toil.utils import addBasicProvisionerOptions

def main():
    parser = getBasicOptionParser()
    parser = addBasicProvisionerOptions(parser)
    config = parseBasicOptions(parser)
    cluster = clusterFactory(provisioner=(config.provisioner), clusterName=(config.clusterName),
      zone=(config.zone))
    cluster.destroyCluster()