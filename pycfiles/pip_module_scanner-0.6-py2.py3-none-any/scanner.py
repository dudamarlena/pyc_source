# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pip_module_scanner/scanner.py
# Compiled at: 2018-09-14 10:19:46
import os, re, sys
try:
    from pip import get_installed_distributions
except ImportError:
    from pip._internal.utils.misc import get_installed_distributions

from pip_module_scanner.exceptions import ScannerException

class Scanner:
    """
    Scanner class
    Looks through all python files to generate a list of unique
    third party libraries for use in
    """

    def __init__(self, path=os.getcwd(), output=None):
        self.import_statement = re.compile('(?:from|import) ([a-zA-Z0-9]+)(?:.*)')
        self.libraries_installed = get_installed_distributions()
        self.libraries_found = []
        self.path = path
        self.path_output = output

    def run(self):
        """
        Runs the scanner
        :return: self
        """
        self.path = os.path.expanduser(self.path)
        if os.path.isdir(self.path):
            self.search_script_directory(self.path)
            return self
        raise ScannerException('Unknown directory: %s' % self.path)

    def output(self):
        """
        Output the results to either STDOUT or
        :return:
        """
        if not self.path_output:
            self.output_to_fd(sys.stdout)
        else:
            with open(self.path_output, 'w') as (out):
                self.output_to_fd(out)

    def output_to_fd(self, fd):
        """
        Outputs the results of the scanner to a file descriptor (stdout counts :)
        :param fd: file
        :return: void
        """
        for library in self.libraries_found:
            fd.write('%s==%s\n' % (library.key, library.version))

    def search_script_directory(self, path):
        """
        Recursively loop through a directory to find all python
        script files. When one is found, it is analyzed for import statements
        :param path: string
        :return: generator
        """
        for subdir, dirs, files in os.walk(path):
            for file_name in files:
                if file_name.endswith('.py'):
                    self.search_script_file(subdir, file_name)

    def search_script_file(self, path, file_name):
        """
        Open a script file and search it for library references
        :param path:
        :param file_name:
        :return: void
        """
        with open(os.path.join(path, file_name), 'r') as (script):
            self.search_script(script.read())

    def search_script(self, script):
        """
        Search a script's contents for import statements and check
        if they're currently prevent in the list of all installed
        pip modules.
        :param script: string
        :return: void
        """
        if self.import_statement.search(script):
            for installed in self.libraries_installed:
                for found in set(self.import_statement.findall(script)):
                    if found == installed.key:
                        self.libraries_installed.remove(installed)
                        self.libraries_found.append(installed)