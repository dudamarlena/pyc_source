# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/commander/commands/run_program.py
# Compiled at: 2016-06-30 06:13:10
from __future__ import print_function
import os, sys
from tingyun.logistics.exceptions import CommandlineParametersException
from tingyun.logistics.mapper import ENV_CONFIG_FILE
from tingyun.config.start_log import log_message
from tingyun import __file__ as root_dir

class Command(object):
    """
    """

    def __init__(self):
        """
        """
        self.name = 'run-program'
        self.options = 'command [parameters]'
        self.description = 'Executes the command with parameters.'

    def execute(self, args):
        """
        :param args:
        :return:
        """
        if 0 == len(args):
            raise CommandlineParametersException()
        log_message('-------------get in bootstrap--------------')
        log_message('TingYun Admin Script (%s)', __file__)
        log_message('working_directory = %r', os.getcwd())
        log_message('current_command = %r', sys.argv)
        log_message('sys.prefix = %r', os.path.normpath(sys.prefix))
        log_message('sys.executable = %r', sys.executable)
        log_message('sys.flags = %r', sys.flags)
        log_message('sys.path = %r', sys.path)
        boot_directory = os.path.join(os.path.dirname(root_dir), 'flashpoint')
        log_message('boot_directory = %r', boot_directory)
        final_python_path = boot_directory
        if 'PYTHONPATH' in os.environ:
            path = os.environ['PYTHONPATH'].split(os.path.pathsep)
            if boot_directory not in path:
                final_python_path = '%s%s%s' % (boot_directory, os.path.pathsep, os.environ['PYTHONPATH'])
        log_message('python_path = %r', final_python_path)
        os.environ['PYTHONPATH'] = final_python_path
        program_exe_path = args[0]
        if not os.path.dirname(program_exe_path):
            program_target_path = os.environ.get('PATH', '').split(os.path.pathsep)
            log_message('get the path from env:%s', program_target_path)
            for path in program_target_path:
                program_exe_path_tmp = os.path.join(path, program_exe_path)
                if os.path.exists(program_exe_path_tmp) and os.access(program_exe_path_tmp, os.X_OK):
                    program_exe_path = program_exe_path_tmp
                    log_message('match the program exe: %s', program_exe_path)
                    break

        log_message('program_exe_path = %r', program_exe_path)
        log_message('execl_arguments = %r', [program_exe_path] + args)
        os.execl(program_exe_path, *args)
        config_file = os.environ.get(ENV_CONFIG_FILE, None)
        if config_file is None:
            print('\n            *************************Warning***********************\n\n                Agent does not obtain the environment\n            variable `%s` for config file. agent did not work.\n                Please set the config file first, and then restart your\n            application with agent\n\n            *******************************************************\n            ' % ENV_CONFIG_FILE)
            return
        else:
            if os.path.isfile(config_file):
                print('\n            *************************Warning***********************\n\n                The config file that environment variable point to is not\n            exist. agent did not work.\n                Please set the config file first, and then restart your\n            application with agent\n\n            *******************************************************\n            ')
                return
            readable = True
            try:
                with open(config_file, 'r'):
                    pass
            except Exception as _:
                readable = False

            if not readable:
                print('\n                *************************Warning***********************\n\n                    The config file `%s`\n                is not readable. agent did not work.\n                    Please set the config file first, and then restart your\n                application with agent\n\n                *******************************************************\n                ' % config_file)
            return