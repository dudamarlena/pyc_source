# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Transformers/ROS/Tools/Topics.py
# Compiled at: 2019-09-27 03:30:17
import dpath.util
from RoboticsLanguage.Base import Utilities
ros_type_mapping = {'Booleans': 'Bool', 
   'Reals32': 'Float32', 
   'Reals64': 'Float64', 
   'Integers8': 'Int8', 
   'Integers16': 'Int16', 
   'Integers32': 'Int32', 
   'Integers64': 'Int64', 
   'Naturals8': 'UInt8', 
   'Naturals16': 'UInt16', 
   'Naturals32': 'UInt32', 
   'Naturals64': 'UInt64', 
   'Strings': 'String'}
cpp_type_mapping = {'Booleans': 'bool', 
   'Reals32': 'float', 
   'Reals64': 'double', 
   'Integers8': 'int8_t', 
   'Integers16': 'int16_t', 
   'Integers32': 'int32_t', 
   'Integers64': 'int64_t', 
   'Naturals8': 'uint8_t', 
   'Naturals16': 'uint16_t', 
   'Naturals32': 'uint32_t', 
   'Naturals64': 'uint64_t', 
   'Strings': 'string'}
python_type_mapping = {'Booleans': 'bool', 
   'Reals32': 'float', 
   'Reals64': 'float', 
   'Integers8': 'int', 
   'Integers16': 'int', 
   'Integers32': 'int', 
   'Integers64': 'int', 
   'Naturals8': 'int', 
   'Naturals16': 'int', 
   'Naturals32': 'int', 
   'Naturals64': 'int', 
   'Strings': 'str'}

def getFlow(signal, variable, code):
    topic_name = signal.xpath('option[@name="rosTopic"]')[0].getchildren()[0].text
    flow = signal.xpath('option[@name="rosFlow"]')[0].getchildren()[0].text
    assignments = code.xpath('//assign/variable[@name="' + variable + '" and count(preceding-sibling::*)=0]|//assign/domain[count(preceding-sibling::*)=0]/variable[@name="' + variable + '" and  count(preceding-sibling::*)=0]|//assign/set[count(preceding-sibling::*)=0]/variable[@name="' + variable + '"]')
    assigned = len(assignments) > 0
    all = code.xpath('//variable[@name="' + variable + '" and not(parent::element)]')
    matching_name_in_domain = code.xpath('//variable[@name="' + variable + '" and (parent::domain) and count(preceding-sibling::*)>0]')
    usages = [ x for x in all if x not in assignments ]
    usages = [ x for x in usages if x not in matching_name_in_domain ]
    used = len(usages) > 0
    flow = 'outgoing' if assigned and not used else flow
    flow = 'incoming' if not assigned and used else flow
    flow = 'bidirectional' if assigned and used else flow
    code.xpath('//element/variable[@name="' + variable + '"]/../Signals/option[@name="rosFlow"]/string')[0].text = flow
    return (
     flow, usages, assignments, topic_name)


def setPublish(variable, flow, assignments, signal):
    if flow in ('outgoing', 'bidirectional'):
        for variable_element in assignments:
            assignment = Utilities.getFirstParent(variable_element, 'assign')
            if 'postRosCpp' not in assignment.attrib.keys():
                assignment.attrib['postRosCpp'] = ''
            if 'postRos2Cpp' not in assignment.attrib.keys():
                assignment.attrib['postRos2Cpp'] = ''
            if 'postRosPy' not in assignment.attrib.keys():
                assignment.attrib['postRosPy'] = ''
            publish = True
            for item in assignment.getparent().getchildren():
                if variable in item.xpath('domain/variable/@name')[:1]:
                    if item is assignment:
                        publish = True
                    else:
                        publish = False

            if publish:
                assignment.attrib['postRosCpp'] += ';' + variable + '_publisher.publish(' + variable + ');'
                assignment.attrib['postRos2Cpp'] += ';' + variable + '_publisher->publish(' + variable + ');'
                assignment.attrib['postRosPy'] += '\n' + variable + '_publisher.publish(' + variable + ')'
            else:
                assignment.attrib['postRosCpp'] += ';'
                assignment.attrib['postRos2Cpp'] += ';'
                assignment.attrib['postRosPy'] += '\n'


def checkTypes(signal, variable, assignments, usages, code, parameters):
    node_name = ''
    if signal.xpath('option[@name="rosType"]/string')[0].text == '':
        local_definitions = code.xpath('//rosm:message/rosm:name/text()', namespaces={'rosm': 'rosm'})
        for element in assignments:
            Utilities.getFirstParent(element, 'assign').attrib['preAssignCpp'] = '.data'
            Utilities.getFirstParent(element, 'assign').attrib['preAssignPython'] = '.data'

        for use in usages:
            use.attrib['returnDomainCpp'] = '.data'
            use.attrib['returnDomainPython'] = '.data'

        topic_type = signal.getchildren()[0]
        if topic_type.tag in ('Reals', 'Integers', 'Naturals'):
            bits = '32'
            for option in topic_type.xpath('option[@name="bits"]'):
                bits = option.getchildren()[0].text

            ros_type = 'std_msgs::' + ros_type_mapping[(topic_type.tag + bits)]
            ros_2_type = 'std_msgs::msg::' + ros_type_mapping[(topic_type.tag + bits)]
            ros_py_type = 'std_msgs.msg.' + ros_type_mapping[(topic_type.tag + bits)]
            cpp_type = cpp_type_mapping[(topic_type.tag + bits)]
        elif topic_type.tag in ('Booleans', 'Strings'):
            ros_type = 'std_msgs::' + ros_type_mapping[topic_type.tag]
            ros_2_type = 'std_msgs::msg::' + ros_type_mapping[topic_type.tag]
            ros_py_type = 'std_msgs.msg.' + ros_type_mapping[topic_type.tag]
            cpp_type = cpp_type_mapping[topic_type.tag]
        elif topic_type.tag == 'RosType':
            ros_type = topic_type.getchildren()[0].text
            if ros_type in local_definitions:
                node_name = Utilities.underscore(code.xpath('//node/option[@name="name"]/string/text()')[0])
                ros_2_type = node_name + '::msg::' + ros_type
                ros_py_type = node_name + '.msg.' + ros_type
                cpp_type = 'void'
                ros_type = node_name + '::' + ros_type
            else:
                ros_type = ros_type.replace('/', '::')
                ros_2_type = ros_type.replace('::', '::msg::')
                ros_py_type = ros_type.replace('::', '.')
                cpp_type = 'void'
        else:
            ros_type = 'std_msgs::Empty'
            ros_2_type = 'std_msgs::msg::Empty'
            ros_py_type = 'std_msgs.msg.Empty'
            cpp_type = 'int'
    else:
        ros_type = signal.xpath('option[@name="rosType"]/string')[0].text.replace('/', '::')
        ros_2_type = signal.xpath('option[@name="rosType"]/string')[0].text.replace('/', '::msg::')
        ros_py_type = signal.xpath('option[@name="rosType"]/string')[0].text.replace('/', '.msg.')
        cpp_type = ros_type
    parameters['Outputs']['RosPy']['Imports'].add(('.').join(ros_py_type.split('.')[:-1]))
    if node_name != ros_type.split('::')[0]:
        parameters['Transformers']['ROS']['buildDependencies'].add(ros_type.split('::')[0])
        parameters['Transformers']['ROS']['runDependencies'].add(ros_type.split('::')[0])
    queue_size = signal.xpath('option[@name="rosQueueSize"]/integer/text()|option[@name="rosQueueSize"]/natural/text()')[0]
    transport_hints_code = signal.xpath('option[@name="rosTransportHints"]')
    transport_hints = ''
    if len(transport_hints_code[0].xpath('./string')) > 0:
        transport_hints = transport_hints_code[0].xpath('./string/text()')[0]
    elif len(transport_hints_code[0].xpath('./vector')) > 0:
        transport_hints = ('.').join(map(lambda x: x.strip() if x.strip()[(-1)] == ')' else x.strip() + '()', transport_hints_code[0].xpath('./vector/string/text()')))
    return (code, parameters, ros_type, cpp_type, ros_2_type, ros_py_type, queue_size, transport_hints)


def process(code, parameters):
    """Processes all the ROS topics in the RoL code"""
    for signal in code.xpath('/node/option[@name="definitions"]/*//element/Signals/option[@name="rosTopic"]/string[text()!=""]/../..'):
        variable = signal.getparent().xpath('variable/@name')[0]
        flow, usages, assignments, topic_name = getFlow(signal, variable, code)
        setPublish(variable, flow, assignments, signal)
        code, parameters, ros_type, cpp_type, ros_2_type, ros_py_type, queue_size, transport_hints = checkTypes(signal, variable, assignments, usages, code, parameters)
        signal.attrib['ROSvariable'] = variable
        parameters['Transformers']['Base']['variables'][variable]['type'] = {'RosCpp': ros_type, 'Ros2Cpp': ros_2_type, 'RosPy': ros_py_type}
        ros2_include = ('/').join((lambda x: x[:-1] + [Utilities.camelCaseToUnderscore(x[(-1)])])(ros_2_type.split('::')))
        if ros_type not in ('ros::Time', 'ros::TimerEvent'):
            parameters['Outputs']['RosCpp']['globalIncludes'].add(ros_type.replace('::', '/') + '.h')
            parameters['Outputs']['Ros2Cpp']['localIncludes'].add(ros2_include + '.hpp')
        parameters['Transformers']['ROS']['topicDefinitions'].append({'variable': variable, 'ros_type': ros_type, 
           'ros_2_type': ros_2_type, 
           'ros_py_type': ros_py_type, 
           'cpp_type': cpp_type, 
           'topic_name': topic_name, 
           'flow': flow, 
           'queue_size': queue_size, 
           'transport_hints': transport_hints})

    return (
     code, parameters)