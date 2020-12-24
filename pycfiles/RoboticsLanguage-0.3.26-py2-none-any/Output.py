# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Outputs/RosPy/Output.py
# Compiled at: 2019-09-27 03:30:17
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates
import os, sys, stat, autopep8, subprocess

def runPreparations(code, parameters):
    parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text
    node_name_underscore = Utilities.underscore(parameters['node']['name'])
    if 'RosPy' in parameters['globals']['deployOutputs'].keys():
        deploy_path = parameters['globals']['deployOutputs']['RosPy']
    else:
        deploy_path = parameters['globals']['deploy']
    return (code, parameters, node_name_underscore, deploy_path)


def output(code, parameters):
    if len(code.xpath('/node')) < 1:
        Utilities.logging.warning('No `node` element found. ROS Python will not generate code!')
        return
    code, parameters, node_name_underscore, deploy_path = runPreparations(code, parameters)
    if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
        sys.exit(1)
    namespace = {'namespaces': {'rosm': 'rosm'}}
    messages = code.xpath('//rosm:message', **namespace)
    if len(messages) > 0:
        folder = Utilities.myOutputPath(parameters) + '/' + node_name_underscore + '/msg'
        Utilities.createFolder(folder)
        for message in messages:
            name = message.xpath('.//rosm:name', **namespace)[0].text
            definition = message.xpath('.//rosm:definition', **namespace)[0].text
            with open(folder + '/' + name + '.msg', 'w') as (file):
                file.write(definition)
                Utilities.logging.debug('Wrote file ' + folder + '/' + name + '.msg ...')

    python_file = deploy_path + '/' + node_name_underscore + '/scripts/' + node_name_underscore + '.py'
    if parameters['Outputs']['RosPy']['showPythonIndentationMarks']:
        with open(python_file, 'r') as (file):
            Utilities.printSource(file.read(), 'python', parameters)
    indent = 0
    indent_step = 4
    python_text = ''
    with open(python_file, 'r') as (file):
        for line in file:
            clean_line = line.strip()
            if clean_line == '#>>':
                indent = indent + indent_step
                continue
            if clean_line == '#<<':
                indent = indent - indent_step
                continue
            python_text += ' ' * indent + clean_line + '\n'

    if parameters['globals']['beautify']:
        python_text = autopep8.fix_code(python_text)
    with open(python_file, 'w') as (file):
        file.write(python_text)
    st = os.stat(python_file)
    os.chmod(python_file, st.st_mode | stat.S_IEXEC)
    if parameters['globals']['compile']:
        if parameters['Outputs']['RosPy']['useColcon']:
            command = [
             'colcon', 'build', '--packages-select', node_name_underscore]
        else:
            command = [
             'catkin', 'build', node_name_underscore]
        Utilities.logging.debug('Compiling with: `' + (' ').join(command) + '` in folder ' + deploy_path + '/..')
        process = subprocess.Popen(command, cwd=deploy_path + '/..')
        process.wait()
        if process.returncode > 0:
            Utilities.logging.error('Compilation failed!!!')
    if parameters['globals']['launch']:
        package_location = (deploy_path + '/' + node_name_underscore).replace('//', '/')
        if package_location not in os.environ['ROS_PACKAGE_PATH']:
            os.environ['ROS_PACKAGE_PATH'] += ':' + package_location
        Utilities.logging.debug('launching: `roslaunch ' + node_name_underscore + ' ' + node_name_underscore + '.launch`')
        process = subprocess.Popen(['roslaunch', node_name_underscore, node_name_underscore + '.launch'])
        process.wait()
    return 0