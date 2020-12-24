# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Base/Tests/test_base_commandline.py
# Compiled at: 2019-09-09 15:48:16
import os, fso, unittest
from RoboticsLanguage.Base import CommandLine, Utilities, Initialise

class TestBaseCommandLine(unittest.TestCase):

    def test_ProcessArguments(self):
        with fso.push() as (overlay):
            Utilities.createFolder('/tmp/RoL/')
            Utilities.createFolder(os.path.expanduser('~') + '/.rol/')
            global_parameters_file = os.path.expanduser('~') + '/.rol/parameters.yaml'
            with open(global_parameters_file, 'w') as (parameter_file):
                parameter_file.write('testing:\n  parameterA: 1\n  repeatedParameter: 1')
            with open('/tmp/RoL/.rol.parameters.yaml', 'w') as (parameter_file):
                parameter_file.write('testing:\n  parameterB: 2\n  repeatedParameter: 2')
            with open('/tmp/RoL/test1.yaml', 'w') as (parameter_file):
                parameter_file.write('testing:\n  parameterC: 3\n  repeatedParameter: 3')
            with open('/tmp/RoL/test2.yaml', 'w') as (parameter_file):
                parameter_file.write('testing:\n  parameterD: 4\n  repeatedParameter: 4')
            with open('/tmp/RoL/test.rol', 'w') as (template_file):
                template_file.write("print('hello')")
            parameters = Initialise.Initialise(True)
            command_line_parameters = [
             'rol', '/tmp/RoL/test.rol',
             '/tmp/RoL/test1.yaml', '/tmp/RoL/test2.yaml', '-o', 'RoLXML']
            flags, arguments, file_package_name, file_formats = CommandLine.prepareCommandLineArguments(parameters)
            parser, args = CommandLine.runCommandLineParser(parameters, arguments, flags, file_formats, file_package_name, command_line_parameters)
            parameters = CommandLine.postCommandLineParser(parameters)
            args.filename[0].name = '/tmp/RoL/test.rol'
            args.filename[1].name = '/tmp/RoL/test1.yaml'
            args.filename[2].name = '/tmp/RoL/test2.yaml'
            filename, filetype, parameters = CommandLine.processCommandLineParameters(args, file_formats, parameters)
            self.assertEqual(filename, '/tmp/RoL/test.rol')
            self.assertEqual(filetype, 'rol')
            self.assertEqual(parameters['globals']['output'], ['RoLXML'])
            self.assertEqual(parameters['testing']['parameterA'], 1)
            self.assertEqual(parameters['testing']['parameterB'], 2)
            self.assertEqual(parameters['testing']['parameterC'], 3)
            self.assertEqual(parameters['testing']['parameterD'], 4)
            self.assertEqual(parameters['testing']['repeatedParameter'], 4)


if __name__ == '__main__':
    unittest.main()