# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Transformers/ROS/Tools/RosClass.py
# Compiled at: 2019-09-09 15:48:17
from RoboticsLanguage.Base import Utilities

def process(code, parameters):
    for item in code.xpath('//RosClass'):
        package_name = item.xpath('./option[@name="package"]/string/text()')[0]
        parameters['Transformers']['ROS']['buildDependencies'].add(package_name)
        parameters['Transformers']['ROS']['runDependencies'].add(package_name)

    return (code, parameters)