# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Transformers/ROS/Tools/Types.py
# Compiled at: 2019-09-27 03:30:17


def process(code, parameters):
    """Processes all the ROS types in the RoL code"""
    packages = []
    message_dependency = []
    for dependency in code.xpath('//rosm:message/rosm:definition/text()', namespaces={'rosm': 'rosm'}):
        for line in dependency.split('\n'):
            if len(line) > 0 and line.lstrip()[0] != '#':
                if len(line.split('/')) > 1:
                    packages.append(line.split('/')[0])
                    message_dependency.append(line.split('/')[0])

    for ros_type in code.xpath('//RosType/string/text()'):
        if len(ros_type.split('/')) > 1:
            packages.append(ros_type.split('/')[0])

    map(lambda x: parameters['Transformers']['ROS']['messageDependencies'].add(x), message_dependency)
    map(lambda x: parameters['Transformers']['ROS']['buildDependencies'].add(x), packages)
    map(lambda x: parameters['Transformers']['ROS']['runDependencies'].add(x), packages)
    return (
     code, parameters)