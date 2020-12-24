# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chris/Development/pymacadmin-env/lib/python2.5/site-packages/PyMacAdmin/SCUtilities/SCPreferences.py
# Compiled at: 2009-06-07 22:49:10
__doc__ = '\nSCPreferences.py: Simplified interaction with SystemConfiguration preferences\n\nTODO:\n* Refactor getvalue/setvalue code into generic functions for dealing with things other than proxies\n* Add get_proxy() to parallel set_proxy()\n'
import sys, os, unittest
from SystemConfiguration import *

class SCPreferences(object):
    """Utility class for working with the SystemConfiguration framework"""
    proxy_protocols = ('HTTP', 'FTP', 'SOCKS')
    session = None

    def __init__(self):
        super(SCPreferences, self).__init__()
        self.session = SCPreferencesCreate(None, 'set-proxy', None)
        return

    def save(self):
        if not self.session:
            return
        if not SCPreferencesCommitChanges(self.session):
            raise RuntimeError('Unable to save SystemConfiguration changes')
        if not SCPreferencesApplyChanges(self.session):
            raise RuntimeError('Unable to apply SystemConfiguration changes')

    def set_proxy(self, enable=True, protocol='HTTP', server='localhost', port=3128):
        new_settings = SCPreferencesPathGetValue(self.session, '/NetworkServices/')
        for interface in new_settings:
            new_settings[interface]['Proxies']['%sEnable' % protocol] = 1 if enable else 0
            if enable:
                new_settings[interface]['Proxies']['%sPort' % protocol] = int(port)
                new_settings[interface]['Proxies']['%sProxy' % protocol] = server

        SCPreferencesPathSetValue(self.session, '/NetworkServices/', new_settings)


class SCPreferencesTests(unittest.TestCase):

    def setUp(self):
        raise RuntimeError('Thwack Chris about not writing these yet')


if __name__ == '__main__':
    unittest.main()