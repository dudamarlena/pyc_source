# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/hardware/oem/dell/test_omreport.py
# Compiled at: 2019-02-11 13:08:12
# Size of source mod 2**32: 699 bytes
import os, unittest
from mercury_agent.hardware.oem.dell import om_xml_deserializer as om

def read_resource(filename):
    with open(os.path.join(os.path.dirname(__file__), 'resources/' + filename), 'rb') as (fp):
        return fp.read()


class TestOMXML(unittest.TestCase):

    def setUp(self):
        self.chassis_xml = read_resource('chassis.xml')

    def test_loader(self):
        xl = om.XLoader(self.chassis_xml)
        self.assertEqual(xl.root.tag, 'OMA')

    def test_chassis_chassis(self):
        xl = om.XLoader(self.chassis_xml)
        chassis = om.XMLChassisStatus(xl.root)
        self.assertEqual(chassis['processor']['status_string'], 'OK')