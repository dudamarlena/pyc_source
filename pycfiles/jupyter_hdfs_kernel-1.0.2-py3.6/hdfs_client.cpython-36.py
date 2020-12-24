# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/connections/hdfs_client.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 936 bytes
"""
    Hdfs Clients
"""
import hdfs_kernel.utils.configuration as config
from hdfs.ext.kerberos import KerberosClient as KerberosClientBase
import posixpath as psp

class HdfsKerberosClient(KerberosClientBase):

    def __init__(self, nameservice, **kwargs):
        urls = self._build_urls(nameservice)
        (super(HdfsKerberosClient, self).__init__)(urls, **kwargs)

    def _build_urls(self, nameservice, port=50070):
        ha_urls = []
        nodes = config.web_hdfs_nodes().get(nameservice)
        assert nodes, 'Hdfs nodes not found'
        for node in nodes:
            url = 'http://{}:{}'.format(node, port)
            ha_urls.append(url)

        return ';'.join(ha_urls)

    def resolve(self, hdfs_path):
        """
            some path start with "resolved", so overwrite it
        """
        return psp.normpath(hdfs_path)