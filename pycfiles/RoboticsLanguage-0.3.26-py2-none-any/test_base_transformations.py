# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Base/Tests/test_base_transformations.py
# Compiled at: 2019-10-30 08:52:56
import unittest, cloudpickle
from lxml import etree
from RoboticsLanguage.Base import Transformations

class TestBaseTransformations(unittest.TestCase):

    def test_Apply(self):
        xml = etree.fromstring('<node><print><string>hello</string></print></node>')
        with open('/tmp/parameters.pickle', 'rb') as (file):
            parameters = cloudpickle.load(file)
        parameters['globals']['output'] = 'RosCpp'
        xml_code, parameters = Transformations.Apply(xml, parameters)
        self.assertEqual(etree.tostring(xml_code), '<node><print RosCpp="ROS_INFO_STREAM(&quot;hello&quot;)"><string RosCpp="&quot;hello&quot;">hello</string><option name="level" RosCpp="&quot;info&quot;"><string RosCpp="&quot;info&quot;">info</string></option></print><option name="name" RosCpp="&quot;unnamed&quot;"><string RosCpp="&quot;unnamed&quot;">unnamed</string></option><option name="rate" RosCpp="25"><real RosCpp="25">25</real></option><option name="initialise" RosCpp=""/><option name="definitions" RosCpp=""/><option name="finalise" RosCpp=""/><option name="cachedComputation" RosCpp=""/></node>')


if __name__ == '__main__':
    unittest.main()