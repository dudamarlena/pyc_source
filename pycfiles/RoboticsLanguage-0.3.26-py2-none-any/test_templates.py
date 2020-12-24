# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Base/Tools/test_templates.py
# Compiled at: 2019-09-27 03:30:17
import os
from jinja2 import Environment, FileSystemLoader
default_template_engine_filters = {}
default_file_patterns = {}
filepatterns = {}
path = '/Users/glopes/Projects/Tests/test_templates/templates/'

def templateEngine(code, parameters, output_name, file_patterns=default_file_patterns, filters=default_template_engine_filters):
    delimeters = {'block_start_string': '<%%', 'block_end_string': '%%>', 
       'variable_start_string': '<<<', 
       'variable_end_string': '>>>', 
       'comment_start_string': '<##', 
       'comment_end_string': '##>'}
    transformers = [
     'FSM', 'test']
    output = 'RosCpp'
    deploy_path = parameters['globals']['deploy']
    templates_path = path + 'Outputs/' + output
    files_to_process = {}
    files_to_copy = []
    for root, dirs, files in os.walk(templates_path):
        for file in files:
            if file.endswith('.template'):
                file_full_path = os.path.join(root, file)
                file_relative_path = file_full_path.replace(templates_path, '').replace('Templates/', '')
                files_to_process[file_relative_path] = {'full_path': file_full_path, 'includes': [], 'header': '', 'elements': []}
            else:
                files_to_copy.append(os.path.join(root, file))

    def CreateGroupFunction(text):
        return lambda x: ('\n').join([ z.format(x) for z in text ])

    for file in files_to_process.keys():
        for module in transformers:
            if os.path.isfile(path + 'Transformers/' + module + '/Templates/Outputs/' + output + file):
                files_to_process[file]['includes'].append(module)
                files_to_process[file]['header'] += ("{{% import '{}' as Include{} with context %}}\n").format(path + 'Transformers/' + module + '/Templates/Outputs/' + output + file, module)
                files_to_process[file]['elements'].append('{{{{Include' + module + '.{}}}}}')

        files_to_process[file]['group_function'] = CreateGroupFunction(files_to_process[file]['elements'])

    for file in files_to_process.keys():
        env = Environment(loader=FileSystemLoader('/'), **delimeters)
        env.filters['group'] = files_to_process[file]['group_function']
        template = env.get_template(files_to_process[file]['full_path'])
        render = template.render(header=files_to_process[file]['header'])
        print '================================='
        print render
        print '================================='
        preprocessed_template = Environment(loader=FileSystemLoader('/')).from_string(render)
        print '-----------------------------------'
        print preprocessed_template.render(message='hello', number='3')
        print '-----------------------------------'