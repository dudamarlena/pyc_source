# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Tools/Templates.py
# Compiled at: 2019-11-19 07:34:18
import os
from pygments import highlight
from RoboticsLanguage.Base import Utilities
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import Terminal256Formatter
from jinja2 import Environment, FileSystemLoader, TemplateError
default_file_patterns = {}
default_ignore_files = {
 '.DS_Store'}
default_template_engine_filters = {'tag': Utilities.tag, 'text': Utilities.text, 
   'dpath': Utilities.path, 
   'xpath': Utilities.xpath, 
   'dpaths': Utilities.paths, 
   'xpaths': Utilities.xpaths, 
   'parent': Utilities.parent, 
   'unique': Utilities.unique, 
   'option': Utilities.option, 
   'dashes': Utilities.dashes, 
   'children': Utilities.children, 
   'initials': Utilities.initials, 
   'fullCaps': Utilities.fullCaps, 
   'isDefined': Utilities.isDefined, 
   'attribute': Utilities.attribute, 
   'camelCase': Utilities.camelCase, 
   'todaysDate': Utilities.todaysDate, 
   'ensureList': Utilities.ensureList, 
   'attributes': Utilities.attributes, 
   'underscore': Utilities.underscore, 
   'unCamelCase': Utilities.unCamelCase, 
   'textWrapBox': Utilities.textWrapBox, 
   'mergeManyOrdered': Utilities.mergeManyOrdered, 
   'optionalArguments': Utilities.optionalArguments, 
   'underscoreFullCaps': Utilities.underscoreFullCaps, 
   'sortListCodeByAttribute': Utilities.sortListCodeByAttribute, 
   'split': lambda x, y: x.split(y)}
delimeters = {'block_start_string': '<%%', 'block_end_string': '%%>', 
   'variable_start_string': '<<<', 
   'variable_end_string': '>>>', 
   'comment_start_string': '<##', 
   'comment_end_string': '##>'}

def createGroupFunction(text):
    """Internal function to the template engine.
  Returns a function that will apply a string to a list of text templates"""
    return lambda x: ('\n').join([ z.format(x) for z in text ])


def templateEngine(code, parameters, output=None, ignore_files=default_ignore_files, file_patterns=default_file_patterns, filters=default_template_engine_filters, templates_path=None, deploy_path=None):
    """The template engine combines multiple template files from different modules to generate code."""
    if output is None:
        output = parameters['developer']['stepName']
    if deploy_path is None:
        if parameters['developer']['stepName'] in parameters['globals']['deployOutputs'].keys():
            deploy_path = parameters['globals']['deployOutputs'][parameters['developer']['stepName']]
        else:
            deploy_path = parameters['globals']['deploy']
    package_parents = Utilities.getPackageOutputParents(parameters, output)
    if templates_path is None:
        templates_paths = [ parameters['manifesto'][parameters['developer']['stepGroup']][x]['path'] + '/Templates' for x in reversed(package_parents) ]
    else:
        templates_paths = [
         templates_path]
    transformers = [ x.split('.')[(-1)] for x in filter(lambda x: 'Transformers' in x, parameters['globals']['loadOrder'])
                   ]
    files_to_process = {}
    files_to_copy = []
    new_files_to_copy = []
    for templates_path in templates_paths:
        for root, dirs, files in os.walk(templates_path):
            for file in files:
                if file.endswith('.template'):
                    file_full_path = os.path.join(root, file)
                    permissions = os.stat(file_full_path)
                    file_relative_path = Utilities.replaceFirst(file_full_path, templates_path, '')
                    file_deploy_path = Utilities.replaceLast(Utilities.replaceFirst(file_full_path, templates_path, deploy_path), '.template', '')
                    for key, value in file_patterns.iteritems():
                        file_deploy_path = file_deploy_path.replace('_' + key + '_', value)

                    files_to_process[file_relative_path] = {'permissions': permissions, 
                       'full_path': file_full_path, 
                       'deploy_path': file_deploy_path, 
                       'includes': [], 'header': [], 'elements': []}
                elif file not in default_ignore_files:
                    copy_file_name = os.path.join(root, file)
                    files_to_copy.append(copy_file_name)
                    new_files_to_copy.append(Utilities.replaceFirst(copy_file_name, templates_path, deploy_path))

    for element in parameters['globals']['loadOrder']:
        if '.Transformers.' in element:
            if 'RoboticsLanguage.' in element:
                path = parameters['globals']['RoboticsLanguagePath']
            else:
                path = parameters['globals']['plugins']
            for output_parent in reversed(package_parents):
                transformer_path = path + '/' + ('/').join(element.split('.')[1:]) + '/Templates/Outputs/' + output_parent
                for root, dirs, files in os.walk(transformer_path):
                    for file in files:
                        if not file.endswith('.template') and file not in default_ignore_files:
                            copy_file_name = os.path.join(root, file)
                            files_to_copy.append(copy_file_name)
                            new_files_to_copy.append(Utilities.replaceFirst(copy_file_name, transformer_path, deploy_path))

    for key, value in file_patterns.iteritems():
        for i in range(len(new_files_to_copy)):
            new_files_to_copy[i] = new_files_to_copy[i].replace('_' + key + '_', value)

    for parent_output in reversed(package_parents):
        for file in files_to_process.keys():
            for module in transformers:
                if os.path.isfile(path + 'Transformers/' + module + '/Templates/Outputs/' + parent_output + '/' + file):
                    if package_parents.index(parent_output) < len(package_parents) - 1:
                        parent = package_parents[(1 + package_parents.index(parent_output))]
                        header_parent = ("{{% import '{}' as Include{} with context %}}\n").format(path + 'Transformers/' + module + '/Templates/Outputs/' + parent + file, module)
                        if header_parent in files_to_process[file]['header']:
                            files_to_process[file]['header'].remove(header_parent)
                    if module not in files_to_process[file]['includes']:
                        files_to_process[file]['includes'].append(module)
                    files_to_process[file]['header'].append(("{{% import '{}' as Include{} with context %}}\n").format(path + 'Transformers/' + module + '/Templates/Outputs/' + parent_output + file, module))
                    elements_text = '{{{{Include' + module + '.{}}}}}'
                    if elements_text not in files_to_process[file]['elements']:
                        files_to_process[file]['elements'].append(elements_text)

            files_to_process[file]['group_function'] = createGroupFunction(files_to_process[file]['elements'])

    for file in files_to_process.keys():
        if os.path.realpath(files_to_process[file]['full_path']) not in parameters['globals']['skipTemplateFiles']:
            try:
                environment = Environment(loader=FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True, **delimeters)
                environment.filters['group'] = files_to_process[file]['group_function']
                template = environment.get_template(files_to_process[file]['full_path'])
                render = template.render(header=('').join(files_to_process[file]['header']))
                if parameters['developer']['intermediateTemplates']:
                    if not parameters['globals']['noColours']:
                        print Utilities.color.BOLD
                        print Utilities.color.YELLOW
                    print '=============================================================================='
                    print 'File: ' + file
                    print 'Full path:' + files_to_process[file]['full_path']
                    print 'Deploy path:' + files_to_process[file]['deploy_path']
                    print '------------------------------------------------------------------------------'
                    if not parameters['globals']['noColours']:
                        print Utilities.color.END
                        try:
                            print highlight(render, get_lexer_for_filename(files_to_process[file]['deploy_path']), Terminal256Formatter(style=Terminal256Formatter().style))
                        except:
                            print render

                    else:
                        print render
                preprocessed_environment = Environment(loader=FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True, finalize=lambda x: x if x is not None else '')
                filters['serializedCode'] = lambda x: Utilities.allAttribute(x, output)
                preprocessed_environment.filters.update(filters)
                preprocessed_template = preprocessed_environment.from_string(render)
                parameters['this'] = parameters['developer']['stepName']
                parameters['this_parents'] = package_parents
                result = preprocessed_template.render(code=code, parameters=parameters)
            except TemplateError as e:
                Utilities.logging.error(e.__repr__())
                return False

            try:
                Utilities.createFolderForFile(files_to_process[file]['deploy_path'])
                with open(files_to_process[file]['deploy_path'], 'w') as (new_package_file):
                    new_package_file.write(result)
                os.chmod(files_to_process[file]['deploy_path'], files_to_process[file]['permissions'].st_mode)
                Utilities.logging.debug(files_to_process[file]['full_path'] + ' -> ' + files_to_process[file]['deploy_path'] + ' ...')
            except OSError as e:
                Utilities.logErrors(Utilities.formatOSErrorMessage(e), parameters)
                return False

    for i in range(0, len(new_files_to_copy)):
        if os.path.realpath(files_to_copy[i]) not in parameters['globals']['skipCopyFiles']:
            try:
                Utilities.createFolderForFile(new_files_to_copy[i])
                Utilities.copyWithPermissions(files_to_copy[i], new_files_to_copy[i])
                Utilities.logging.debug('Copied file ' + new_files_to_copy[i] + '...')
            except OSError as e:
                Utilities.logErrors(Utilities.formatOSErrorMessage(e), parameters)
                return False

    return True