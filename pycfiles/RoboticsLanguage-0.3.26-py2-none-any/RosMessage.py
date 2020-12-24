# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Transformers/ROS/Tools/RosMessage.py
# Compiled at: 2019-09-09 15:48:17
from RoboticsLanguage.Base import Utilities

def process(code, parameters):
    namespace = {'namespaces': {'rosm': 'rosm'}}
    messages = code.xpath('//rosm:message', **namespace)
    if len(messages) > 0:
        parameters['Transformers']['ROS']['addingNewMessages'] = True
    return (code, parameters)