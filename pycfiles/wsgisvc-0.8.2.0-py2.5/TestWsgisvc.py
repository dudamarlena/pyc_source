# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\TestWsgisvc.py
# Compiled at: 2009-06-06 04:17:18
import unittest
from wsgisvc import *

class TestWsgisvcCase(unittest.TestCase):

    def test_config1(self):
        ds = ServiceSettings(os.path.abspath('wsgi_ini_files\\test1.ini'))
        self.assertEquals(ds.getSvcName(), 'svcname1')
        self.assertEquals(ds.getSvcDisplayName(), 'svc display name1')
        self.assertTrue(ds.getSvcDescription().startswith('wsgi_ini_file: %s; log_file: %s' % (os.path.join(ds.getCfgFileDir(), ds.getCfgFileName()), ds.getStdOutFileName())))
        self.assertEquals(ds.getStdOutFileName(), 'svcname1_std.log')
        self.assertTrue(ds.getVirtualEnv() is None)
        return

    def test_config2(self):
        ds = ServiceSettings(os.path.abspath('wsgi_ini_files\\test2.ini'))
        self.assertEquals(ds.getSvcName(), 'svcname2')
        self.assertEquals(ds.getSvcDisplayName(), 'svc display name2')
        self.assertEquals(ds.getSvcDescription(), 'description of service 2; wsgi_ini_file: %s; log_file: %s' % (ds.getCfgFileName(), ds.getStdOutFileName()))
        self.assertEquals(ds.getStdOutFileName(), 'logfilename2')
        self.assertEquals(ds.getVirtualEnv(), 'c:\\virtualenv2')

    def test_name_default(self):
        ds = ServiceSettings(os.path.abspath('wsgi_ini_files\\no_winservice_section.ini'))
        self.assertEquals(ds.getSvcName(), 'no_winservice_section')

    def test_transfer(self):
        ds = ServiceSettings(os.path.abspath('wsgi_ini_files\\test1.ini'))

        class A:
            pass

        ds.transferEssential(A)
        self.assertEquals(A._svc_name_, ds.getSvcName())
        self.assertEquals(A._svc_display_name_, ds.getSvcDisplayName())
        self.assertEquals(A._svc_description_, ds.getSvcDescription())

    def test_get_service_class(self):
        ServiceClass = getServiceClassString(PasteWinService, sys.argv)

    def test_get_services(self):
        listServices()

    def test_nonexistent(self):
        ds = ServiceSettings('nonexistentfile.ini')
        self.assertEquals(ds.getSvcName(), 'nonexistentfile')


if __name__ == '__main__':
    unittest.main()