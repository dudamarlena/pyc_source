# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_ubootenv.py
# Compiled at: 2017-02-08 04:42:30
""" Dummy implementation of cxmanage_api.ubootenv.UbootEnv """
from cxmanage_api.ubootenv import UbootEnv

class DummyUbootEnv(UbootEnv):
    """UbootEnv info."""

    def get_boot_order(self):
        """Hard coded boot order for testing."""
        return [
         'disk', 'pxe']

    def set_boot_order(self, boot_args):
        """ Do nothing """
        pass