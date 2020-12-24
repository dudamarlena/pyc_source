# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_ubootenv.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Dummy implementation of cxmanage_api.ubootenv.UbootEnv '
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