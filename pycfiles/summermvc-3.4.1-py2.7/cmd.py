# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/cmd.py
# Compiled at: 2018-06-01 04:01:51
__all__ = [
 'DispatchCommand']
__authors__ = ['Tim Chow']
from optparse import OptionParser
import sys, os, shutil
from pkg_resources import resource_filename

class DispatchCommand(object):

    def __init__(self, subcommand, options):
        self._subcommand = subcommand
        self._options = options

    def _subcommand__demo(self):
        src = resource_filename('summermvc', 'templates/project_demo')
        dst = self._options.name
        print '\x1b[32mdemo is running\x1b[0m'
        if os.path.exists(dst):
            sys.exit('\x1b[31m[%s] exists\x1b[0m' % dst)
        dst = os.path.abspath(dst)
        print '\x1b[32mcopying files\x1b[0m'
        shutil.copytree(src, dst)
        print '\x1b[32mdeleting .pyc/.pyo \x1b[0m'
        for base_directory, sub_directories, files in os.walk(dst):
            for file in files:
                file_name = os.path.join(base_directory, file)
                if os.path.splitext(file_name)[1] in ('.pyc', '.pyo'):
                    os.remove(file_name)

        application_path = os.path.join(dst, 'application.py')
        if os.path.isfile(application_path):
            with open(application_path, 'rb') as (fd):
                content = fd.read().replace('{{PROJECT_BASE_DIRECTORY}}', dst)
            with open(application_path, 'wb') as (fd):
                fd.write(content)
        print '\x1b[32mdemo is created in [%s]\x1b[0m' % dst
        return 0

    def line_count(self, file_name):
        count = 0
        with open(file_name) as (fd):
            for line in fd:
                count = count + 1

        return count

    def _subcommand__linecount(self):
        exclude_pattern = self._options.exclude_pattern or ''
        exclude_patterns = exclude_pattern.replace(' ', '').split(',')
        exclude_patterns = [ '.%s' % e for e in exclude_patterns ]
        base_directory = self._options.base_directory
        if not base_directory:
            sys.exit('\x1b[31mno base directory or file provided\x1b[0m')
        if not os.path.exists(base_directory):
            sys.exit('\x1b[31m[%s] is not directory or file\x1b[0m' % base_directory)
        if os.path.isfile(base_directory):
            if os.path.splitext(base_directory)[1] in exclude_patterns:
                sys.exit('\x1b[32mskipped file: [%s]\x1b[0m' % base_directory)
            sys.exit('\x1b[32m[%s] [%d]\x1b[0m' % (
             base_directory, self.line_count(base_directory)))
        total_count = 0
        for dir_name, sub_dirnames, file_names in os.walk(base_directory):
            for file_name in file_names:
                file_name = os.path.join(dir_name, file_name)
                if os.path.splitext(file_name)[1] in exclude_patterns:
                    print '\x1b[32mskipped file: [%s]\x1b[0m' % file_name
                    continue
                count = self.line_count(file_name)
                print '\x1b[32m[%s] [%d]\x1b[0m' % (file_name, count)
                total_count = total_count + count

        print '\x1b[32mtotal count: [%d]\x1b[0m' % total_count

    def run(self):
        f = getattr(self, '_subcommand__%s' % self._subcommand, None)
        if f is None:
            sys.exit('\x1b[31mthere is no subcommand named: %s\x1b[0m' % self._subcommand)
        return f() or 0


def main(args=None):
    parser = OptionParser(usage='%prog subcommand [options]')
    parser.add_option('-n', '--name', default='summermvc_demo', type=str, dest='name', help='project name')
    parser.add_option('-d', '--directory', type=str, dest='base_directory', help='base directory or file')
    parser.add_option('-e', '--exclude', type=str, dest='exclude_pattern', help='exclude_pattern')
    options, args = parser.parse_args(args or sys.argv[1:])
    if len(args) < 1:
        parser.error('no subcommand provided')
    dispatch_command = DispatchCommand(args[0], options)
    return dispatch_command.run()