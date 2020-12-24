# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/parsers/paths.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 2177 bytes
import re
from hdfs_kernel.constants import HDFS_PREFIX, RESOLVED_PREFIX
import hdfs_kernel.utils.configuration as config

def is_hdfs_path(path):
    is_correct_prefix = any([
     path.startswith(HDFS_PREFIX),
     path.startswith(RESOLVED_PREFIX),
     path.startswith('/')])
    if not is_correct_prefix:
        return False
    else:
        return True


def is_local_path(path):
    pattern = '([./|/][a-zA-Z\\./]*[\\s]?)'
    return re.findall(pattern, path)


class HdfsPath(dict):
    __doc__ = '\n        hdfs path parser\n        resolve name service and real path\n        eg: "resolved://nfjd-prod-ns2/user/hive/", "hdfs://nfjd-prod-ns3/user/"\n    '

    def __init__(self, path):
        self.path = path
        self.protocols = [HDFS_PREFIX, RESOLVED_PREFIX]
        self.item = self.resolve()
        super(HdfsPath, self).__init__(self.item)

    def resolve(self):
        nameservice = self.get_nameservice()
        real_path = self.get_real_path(nameservice=nameservice)
        path_service = self.path.replace(real_path, '')
        struct = {'source_path':self.path, 
         'nameservice':nameservice, 
         'path':real_path, 
         'path_service':path_service}
        return struct

    def get_nameservice(self):
        nameservice_list = config.web_hdfs_name_services()
        pattern = '|'.join(nameservice_list)
        match = re.findall(pattern, (self.path), flags=1)
        if match:
            return match.pop()
        else:
            return config.default_name_service()

    def get_real_path(self, nameservice=None):
        replace_times = 1
        path = self.strip_protocols_prefix(self.path)
        if nameservice:
            if path.startswith(nameservice):
                path = path.replace(nameservice, '', replace_times)
        return path

    def strip_protocols_prefix(self, path):
        replace_times = 1
        for protocol in self.protocols:
            if path.startswith(protocol):
                path = path.replace(protocol, '', replace_times)

        return path