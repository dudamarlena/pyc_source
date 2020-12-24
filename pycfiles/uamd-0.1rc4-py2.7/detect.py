# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test/detect.py
# Compiled at: 2011-11-22 04:04:45
import unittest, uamd

class TestCase(unittest.TestCase):

    def test_docomo_mova(self):
        META = {'HTTP_USER_AGENT': 'DoCoMo/1.0/D502i', 
           'HTTP_X_DCMGUID': 'XXXXXXX', 
           'REMOTE_ADDR': '210.153.84.0'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'D502i')
        self.assertEqual(device.type, 'MOVA')
        self.assertFalse(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.spoof)

    def test_docomo_foma(self):
        META = {'HTTP_USER_AGENT': 'DoCoMo/2.0 F06B(c500;TB;W24H16)', 
           'HTTP_X_DCMGUID': 'XXXXXXX', 
           'REMOTE_ADDR': '210.153.84.0'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'F06B')
        self.assertEqual(device.type, 'FOMA')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.spoof)

    def test_docomo_spoof(self):
        META = {'HTTP_USER_AGENT': 'DoCoMo/2.0 F06B(c500;TB;W24H16)', 
           'HTTP_X_DCMGUID': 'XXXXXXX', 
           'REMOTE_ADDR': '127.0.0.1'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'F06B')
        self.assertEqual(device.type, 'FOMA')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertTrue(device.spoof)

    def test_kddi(self):
        META = {'HTTP_USER_AGENT': 'KDDI-SA31 UP.Browser/6.2.0.7.3.129 (GUI) MMP/2.0', 
           'HTTP_X_UP_SUBNO': 'XXXXXXX', 
           'REMOTE_ADDR': '210.230.128.224'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'SA31')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.hdml)
        self.assertFalse(device.spoof)

    def test_kddi_hdml(self):
        META = {'HTTP_USER_AGENT': 'SIE-SA31 UP.Browser/6.2.0.7.3.129 (GUI) MMP/2.0', 
           'HTTP_X_UP_SUBNO': 'XXXXXXX', 
           'REMOTE_ADDR': '210.230.128.224'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'SA31')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertTrue(device.hdml)
        self.assertFalse(device.spoof)

    def test_kddi_fake(self):
        META = {'HTTP_USER_AGENT': 'KDDI-SA31 UP.Browser/6.2.0.7.3.129 (GUI) MMP/2.0', 
           'HTTP_X_UP_SUBNO': 'XXXXXXX', 
           'REMOTE_ADDR': '127.0.0.1'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'SA31')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.hdml)
        self.assertTrue(device.spoof)

    def test_softbank_jphone(self):
        META = {'HTTP_USER_AGENT': 'J-PHONE/2.0/J-SH02', 
           'HTTP_X_JPHONE_UID': 'XXXXXXX', 
           'REMOTE_ADDR': '123.108.237.0'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'J-SH02')
        self.assertEqual(device.type, 'J-PHONE')
        self.assertFalse(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.spoof)

    def test_softbank_vodafone(self):
        META = {'HTTP_USER_AGENT': 'Vodafone/1.0/V803T/TJ001[/Serial] Browser/VF-Browser/1.0', 
           'HTTP_X_JPHONE_UID': 'XXXXXXX', 
           'REMOTE_ADDR': '123.108.237.0'}
        device = uamd.detect(META)
        self.assertEqual(device.name, 'V803T')
        self.assertEqual(device.type, 'Vodafone')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.spoof)

    def test_softbank_softbank(self):
        META = {'HTTP_USER_AGENT': 'SoftBank/1.0/002Pe/PJP10[/Serial] Browser/NetFront/3.4 Profile/MIDP-2.0 Configuration/CLDC-1.1', 
           'HTTP_X_JPHONE_UID': 'XXXXXXX', 
           'REMOTE_ADDR': '123.108.237.0'}
        device = uamd.detect(META)
        self.assertEqual(device.name, '002Pe')
        self.assertEqual(device.type, 'SoftBank')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertFalse(device.spoof)

    def test_softbank_softbank_fake(self):
        META = {'HTTP_USER_AGENT': 'SoftBank/1.0/002Pe/PJP10[/Serial] Browser/NetFront/3.4 Profile/MIDP-2.0 Configuration/CLDC-1.1', 
           'HTTP_X_JPHONE_UID': 'XXXXXXX', 
           'REMOTE_ADDR': '127.0.0.1'}
        device = uamd.detect(META)
        self.assertEqual(device.name, '002Pe')
        self.assertEqual(device.type, 'SoftBank')
        self.assertTrue(device.support_cookie)
        self.assertEqual(device.uid, 'XXXXXXX')
        self.assertTrue(device.spoof)


if __name__ == '__main__':
    unittest.main()