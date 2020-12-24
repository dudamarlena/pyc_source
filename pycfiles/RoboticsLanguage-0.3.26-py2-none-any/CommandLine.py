# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/CommandLine.py
# Compiled at: 2019-11-03 18:09:03
import os, sys, yaml, glob, shutil, argparse, dpath.util, argcomplete
from copy import copy
from . import Utilities
from . import Parameters
parameters_home_file = '.rol/parameters.yaml'
parameters_local_file = ['.rol.parameters.yaml', 'rol.parameters.yaml']

def generateArgparseArguments(parameters, flags):
    flat = Utilities.flatDictionary(parameters)
    arguments = {}
    command_line_flags = {}
    for key, value in flat.iteritems():
        special_key = key.replace('-', ':')[1:]
        arguments[special_key] = {}
        arguments[special_key]['dest'] = key
        command_line_flags[special_key] = [
         '-' + str(key)]
        arguments[special_key]['default'] = None
        if special_key in flags.keys():
            if Utilities.isKeyDefined('longFlag', flags[special_key]):
                command_line_flags[special_key] = [
                 '--' + flags[special_key]['longFlag']]
            if Utilities.isKeyDefined('flag', flags[special_key]):
                command_line_flags[special_key].insert(0, '-' + flags[special_key]['flag'])
            if Utilities.isKeyDefined('numberArguments', flags[special_key]):
                arguments[special_key]['nargs'] = flags[special_key]['numberArguments']
            if Utilities.isKeyDefined('noArgument', flags[special_key]):
                if flags[special_key]['noArgument']:
                    if value is False:
                        arguments[special_key]['action'] = 'store_true'
                    else:
                        arguments[special_key]['action'] = 'store_false'
            else:
                arguments[special_key]['type'] = type(value)
                arguments[special_key]['metavar'] = str(type(value).__name__.upper())
            if Utilities.isKeyDefined('description', flags[special_key]):
                arguments[special_key]['help'] = flags[special_key]['description']
            if Utilities.isKeyDefined('choices', flags[special_key]):
                arguments[special_key]['choices'] = flags[special_key]['choices']
            if Utilities.isKeyDefined('suppress', flags[special_key]):
                if flags[special_key]['suppress']:
                    arguments.pop(special_key)
                    command_line_flags.pop(special_key)
        else:
            arguments[special_key]['type'] = type(value)
            arguments[special_key]['metavar'] = str(type(value).__name__.upper())

    return (
     command_line_flags, arguments)


@Utilities.cache_in_disk
def prepareCommandLineArguments(parameters):
    Parameters.command_line_flags['globals:output']['choices'] = parameters['manifesto']['Outputs'].keys()
    Parameters.command_line_flags['globals:input']['choices'] = parameters['manifesto']['Inputs'].keys()
    Parameters.command_line_flags['globals:setEnvironment']['choices'] = sum([ x.keys() for x in dpath.util.values(parameters, 'manifesto/*/*/environments') ], [])
    subset = dict((x, parameters[x]) for x in ['Information', 'Transformers', 'Inputs', 'Outputs', 'globals', 'developer'])
    flags, arguments = generateArgparseArguments(subset, parameters['command_line_flags'])
    file_formats = []
    file_package_name = []
    for key, value in parameters['manifesto']['Inputs'].iteritems():
        file_formats.append(value['fileFormat'])
        file_package_name.append(value['fileFormat'] + ': ' + value['packageName'] + ' file format')

    file_package_name.append('yaml: optional parameter files; \n')
    return (
     flags, arguments, file_package_name, file_formats)


def runCommandLineParser(parameters, arguments, flags, file_formats, file_package_name, command_line_arguments):
    parser = argparse.ArgumentParser(prog='rol', description='Robotics Language compiler', formatter_class=argparse.RawTextHelpFormatter)
    groups = {}
    for key in sorted(parameters):
        groups[key] = parser.add_argument_group(key.lower())

    for key in sorted(arguments):
        groups[key.split(':')[0]].add_argument(*flags[key], **arguments[key])

    try:
        list_of_no_file_needed_flags = reduce(lambda a, b: a + b, [ flags[x] for x in dpath.util.search(parameters, 'command_line_flags/*/fileNotNeeded')['command_line_flags'].keys()
                                                                  ])
    except:
        list_of_no_file_needed_flags = []

    if any([ x in list_of_no_file_needed_flags for x in sys.argv ]):
        nargs = '*'
        parameters['globals']['fileNeeded'] = False
    else:
        nargs = '+'
        parameters['globals']['fileNeeded'] = True
    parser.add_argument('filename', metavar='[ ' + (' | ').join(map(lambda x: 'file.' + x, file_formats)) + ' ] [ profile.yaml ... ]', type=argparse.FileType('r'), nargs=nargs, help=(';\n').join(file_package_name))
    argcomplete.autocomplete(parser)
    args = parser.parse_args(command_line_arguments[1:])
    return (
     parser, args)


def processFileParameters(args, file_formats, parameters):
    rol_files = []
    parameter_files = []
    unknown_files = []
    for element in args.filename:
        name, extension = os.path.splitext(os.path.abspath(element.name))
        if extension.lower() in map(lambda x: '.' + x.lower(), file_formats):
            rol_files.append({'file': element, 'name': name + extension, 'type': extension[1:]})
        elif extension.lower() in ('.yaml', '.yml'):
            parameter_files.append({'file': element, 'name': name + extension})
        else:
            unknown_files.append(name + extension)

    if len(unknown_files) > 0:
        Utilities.logging.error('the following files have unknown formal: ' + str(unknown_files))
        sys.exit(1)
    if len(rol_files) == 0 and parameters['globals']['fileNeeded']:
        Utilities.logging.error('no Robotics Language files detected!')
        sys.exit(1)
    else:
        if len(rol_files) > 1:
            Utilities.logging.warn('the following files are disregarded:\n' + ('\n').join([ x['name'] for x in rol_files[1:] ]))
        for rol_file in rol_files:
            path, name = os.path.split(rol_file['name'])
            for local in parameters_local_file:
                local_file = path + '/' + local
                if os.path.isfile(local_file):
                    parameter_files.insert(0, {'file': open(local_file, 'r'), 'name': local_file})

    home_file = os.path.expanduser('~') + '/' + parameters_home_file
    if os.path.isfile(home_file):
        parameter_files.insert(0, {'file': open(home_file, 'r'), 'name': home_file})
        first_time = False
    else:
        first_time = True
    return (rol_files, parameter_files, first_time)


def runAllWizards(personalized_parameters, parameters):
    for module_name in parameters['globals']['loadOrder']:
        name_split = module_name.split('.')
        try:
            wizard_module = __import__(module_name + '.Wizard', globals(), locals(), ['Wizard'])
            personalized_parameters, parameters = wizard_module.wizard(personalized_parameters, parameters)
        except Exception as e:
            Utilities.logging.debug(e.__repr__())

    return (personalized_parameters, parameters)


def processCommandLineParameters(args, file_formats, parameters):
    command_line_parameters_flat = {}
    for key, value in vars(args).iteritems():
        if value is not None:
            command_line_parameters_flat[key] = value

    command_line_parameters = Utilities.unflatDictionary(command_line_parameters_flat)
    if Utilities.isDefined(command_line_parameters, '/globals/verbose'):
        Utilities.setLoggerLevel(command_line_parameters['globals']['verbose'])
    rol_files, parameter_files, first_time = processFileParameters(args, file_formats, parameters)
    for parameter_file in parameter_files:
        parameters = Utilities.mergeDictionaries(yaml.safe_load(parameter_file['file']), parameters)

    parameters = Utilities.mergeDictionaries(command_line_parameters, parameters)
    for openfile in parameters['filename']:
        openfile.close()

    parameters.pop('filename', None)
    parameters['globals']['output'] = Utilities.ensureList(parameters['globals']['output'])
    parameters['developer']['progressTotal'] = 1 + len(parameters['manifesto']['Transformers']) + len(parameters['globals']['output'])
    if first_time:
        personalized_parameters, parameters = runAllWizards({}, parameters)
        Utilities.createFolder(os.path.expanduser('~/.rol'))
        with open(os.path.expanduser('~/.rol/parameters.yaml'), 'w') as (output):
            yaml.dump(personalized_parameters, output, default_flow_style=False)
        Utilities.logging.warning('Created parameters file "~/.rol/parameters.yaml".')
        parameters['globals']['firstTime'] = personalized_parameters
    if len(rol_files) == 0:
        return (None, None, parameters)
    else:
        return (
         rol_files[0]['name'], rol_files[0]['type'], parameters)
        return


def getTemplateTextForOutputPackage(parameters, keyword, package):
    if package in parameters['language'][keyword]['output'].keys():
        return (parameters['language'][keyword]['output'][package], package)
    if 'parent' in parameters['manifesto']['Outputs'][package].keys():
        return getTemplateTextForOutputPackage(parameters, keyword, parameters['manifesto']['Outputs'][package]['parent'])
    raise


def loadRemainingParameters(parameters):
    language = {}
    messages = {}
    error_handling = {}
    error_exceptions = {}
    default_output = {}
    for module_name in parameters['globals']['loadOrder']:
        name_split = module_name.split('.')
        try:
            language_module = __import__(module_name + '.Language', globals(), locals(), ['Language'])
            for keyword in language_module.language.keys():
                language_module.language[keyword]['package'] = name_split[1] + ':' + name_split[2]

            language = Utilities.mergeDictionaries(language, language_module.language)
            if name_split[1] == 'Outputs':
                default_output[name_split[2]] = language_module.default_output
        except Exception as e:
            Utilities.logging.debug(e.__repr__())

        try:
            messages_module = __import__(module_name + '.Messages', globals(), locals(), ['Messages'])
            messages = Utilities.mergeDictionaries(messages, messages_module.messages)
        except Exception as e:
            Utilities.logging.debug(e.__repr__())

        try:
            error_module = __import__(module_name + '.ErrorHandling', globals(), locals(), ['ErrorHandling'])
            error_handling = Utilities.mergeDictionaries(error_handling, error_module.error_handling_functions)
            error_exceptions = Utilities.mergeDictionaries(error_exceptions, error_module.error_exception_functions)
        except Exception as e:
            Utilities.logging.debug(e.__repr__())

    parameters['language'] = language
    parameters['messages'] = messages
    parameters['errorExceptions'] = error_exceptions
    parameters['errorHandling'] = error_handling
    for keyword, value in parameters['language'].iteritems():
        if 'output' in value.keys():
            missing = list(set(parameters['Outputs'].keys()) - set(value['output'].keys()))
        else:
            missing = parameters['Outputs'].keys()
            parameters['language'][keyword]['output'] = {}
        parameters['language'][keyword]['defaultOutput'] = []
        parameters['language'][keyword]['inheritedOutput'] = []
        for item in missing:
            try:
                parameters['language'][keyword]['output'][item], inherited_package = getTemplateTextForOutputPackage(parameters, keyword, item)
                parameters['language'][keyword]['inheritedOutput'].append({item: inherited_package})
            except:
                parameters['language'][keyword]['output'][item] = default_output[item]
                parameters['language'][keyword]['defaultOutput'].append(item)

    return parameters


def postCommandLineParser(parameters):
    if parameters['globals']['version']:
        import pkg_resources
        print 'The Robotics Language version: ' + pkg_resources.get_distribution('RoboticsLanguage').version
    if parameters['developer']['showDeployPath']:
        print parameters['globals']['deploy']
    if parameters['globals']['setEnvironment'] != '':
        for environment in dpath.util.values(parameters, 'manifesto/*/*/environments'):
            if parameters['globals']['setEnvironment'] in environment.keys():
                parameters_filename = os.path.expanduser('~') + '/.rol/parameters.yaml'
                try:
                    if os.path.exists(parameters_filename):
                        with open(parameters_filename, 'r') as (file):
                            current_environment = yaml.safe_load(file)
                        new_environment = Utilities.mergeDictionaries(environment[parameters['globals']['setEnvironment']], current_environment)
                        old_parameters_filename = Utilities.getNonexistantPath(parameters_filename)
                        shutil.move(parameters_filename, old_parameters_filename)
                    else:
                        new_environment = environment[parameters['globals']['setEnvironment']]
                    with open(parameters_filename, 'w') as (file):
                        file.write(yaml.safe_dump(new_environment, default_flow_style=False))
                    print "Create new parameters file at '" + parameters_filename + "'.\nOld parameters file saved in '" + old_parameters_filename + "'"
                except Exception as e:
                    Utilities.logging.warning('Unable to set environment to "' + parameters['globals']['setEnvironment'] + '". Please check the permissions of the file "' + parameters_filename + '"')
                    print e

    if parameters['developer']['info']:
        import pkg_resources
        print 'The Robotics Language version: ' + pkg_resources.get_distribution('RoboticsLanguage').version
        for key, value in parameters['manifesto'].iteritems():
            print key + ':'
            for item, content in value.iteritems():
                extra = ' *' if parameters['globals']['plugins'] in content['path'] else ''
                print '  ' + item + ' (' + content['version'] + ')' + extra

    if parameters['developer']['infoPackage'] != '':
        for type in ['Inputs', 'Transformers', 'Outputs']:
            if parameters['developer']['infoPackage'] in parameters['manifesto'][type].keys():
                package = parameters['manifesto'][type][parameters['developer']['infoPackage']]
                print 'Package ' + type + '/' + parameters['developer']['infoPackage']
                print 'Version: ' + package['version']
                print 'Path: ' + package['path']
                print 'Information:'
                Utilities.printParameters(package['information'])

    if parameters['developer']['makeConfigurationFile']:
        data = parameters['command_line_flags']
        filtered = filter(lambda x: x[0:11] == 'Information' or 'suppress' not in data[x].keys() or data[x]['suppress'] is not True, data.iterkeys())
        commands = {x:dpath.util.get(parameters, x.replace(':', '/')) for x in filtered}
        commands_dictionary = Utilities.unflatDictionary(commands, ':')
        commands_dictionary['developer']['makeConfigurationFile'] = False
        try:
            Utilities.createFolder(os.path.expanduser('~/.rol'))
            if os.path.isfile(os.path.expanduser('~/.rol/parameters.yaml')):
                with open(os.path.expanduser('~/.rol/parameters.yaml.template'), 'w') as (output):
                    yaml.dump(commands_dictionary, output, default_flow_style=False)
                print 'Created the file "~/.rol/parameters.yaml.template".'
                print 'Please modify this file and rename it to "~/.rol/parameters.yaml"'
            else:
                with open(os.path.expanduser('~/.rol/parameters.yaml'), 'w') as (output):
                    yaml.dump(commands_dictionary, output, default_flow_style=False)
                print 'Created the file "~/.rol/parameters.yaml".'
        except Exception as e:
            print 'Error creating configuration file!'
            print e

    if parameters['developer']['showOutputDependency']:
        for package in parameters['manifesto']['Outputs']:
            if 'parent' in parameters['manifesto']['Outputs'][package].keys():
                print parameters['manifesto']['Outputs'][package]['parent'] + ' <- ' + package

    if parameters['developer']['copyExamplesHere']:
        from_path = parameters['globals']['RoboticsLanguagePath'] + 'Examples'
        here_path = os.getcwd()
        for item in os.listdir(from_path):
            s = os.path.join(from_path, item)
            d = os.path.join(here_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    if parameters['developer']['runTests']:
        from unittest import defaultTestLoader, TextTestRunner
        import coverage, cloudpickle
        with open('/tmp/parameters.pickle', 'wb') as (file):
            cloudpickle.dump(parameters, file)
        if parameters['developer']['coverage']:
            cov = coverage.Coverage(omit=['*/lib/python*', '*Tests/test_*', '*__init__.py'])
            cov.start()
        suite = defaultTestLoader.discover(parameters['globals']['RoboticsLanguagePath'], 'test_*.py')
        TextTestRunner(verbosity=2).run(suite)
        if parameters['developer']['coverage']:
            cov.stop()
            cov.save()
            cov.html_report(directory=parameters['developer']['coverageFolder'], ignore_errors=True)
            print 'Coverage report is: ' + parameters['developer']['coverageFolder'] + '/index.html'
        os.remove('/tmp/parameters.pickle')
        sys.exit(1)
    if parameters['developer']['makeExamples']:
        import subprocess
        command_line_arguments = copy(parameters['commandLineParameters'])
        command_line_arguments.remove('--make-examples')
        list_commands = []
        for name in glob.glob(parameters['globals']['RoboticsLanguagePath'] + '/*/*/Examples/*.*'):
            list_commands.append([command_line_arguments[0], name] + command_line_arguments[1:])

        for command, index in zip(list_commands, range(len(list_commands))):
            print '[' + str(index + 1) + '/' + str(len(list_commands)) + '] ' + command[1]
            process = subprocess.Popen(command)
            process.wait()

        sys.exit(1)
    return parameters


def ProcessArguments(command_line_parameters, parameters):
    parameters['commandLineParameters'] = command_line_parameters
    flags, arguments, file_package_name, file_formats = prepareCommandLineArguments(parameters)
    parser, args = runCommandLineParser(parameters, arguments, flags, file_formats, file_package_name, command_line_parameters)
    parameters = loadRemainingParameters(parameters)
    file_name, file_type, parameters = processCommandLineParameters(args, file_formats, parameters)
    parameters = postCommandLineParser(parameters)
    return (
     file_name, file_type, parameters)