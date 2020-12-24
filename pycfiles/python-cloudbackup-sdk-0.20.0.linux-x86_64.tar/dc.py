# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cloudbackup/utils/dc.py
# Compiled at: 2017-05-12 15:59:18
"""
Data Center Utils
"""
import logging, os, subprocess

class DC(object):
    """
    VM access to determine the Data Center the server lives in
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def get_dc(self):
        """
        Return the Data Center the current server is running on

        Note: Requires xenstore-read to be present on the system (Linux, Citrix XenServer Tools)
        """
        if os.getgid():
            raise RuntimeError('User must be root to access XenStore functionality')
        xen_args = ['xenstore-read', 'vm-data/provider_data/region']
        dc_xenstore = subprocess.Popen(xen_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dc_xenstore_result = dc_xenstore.communicate()
        if dc_xenstore.returncode == 0:
            self.log.info(('System is running in: {0:}').format(dc_xenstore_result[0].strip()))
            return dc_xenstore_result[0].strip()
        raise RuntimeError(('Unable to access Xenstore (code: {0:}) - {1:}').format(dc_xenstore.returncode, dc_xenstore_result[0]))