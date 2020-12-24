# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/main/setuptools_command.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 4005 bytes
"""The logic for Flake8's integration with setuptools."""
import os
from typing import List, Tuple
import setuptools
from flake8.main import application as app
UNSET = object()

class Flake8(setuptools.Command):
    __doc__ = 'Run Flake8 via setuptools/distutils for registered modules.'
    description = 'Run Flake8 on modules registered in setup.py'
    user_options = []

    def initialize_options(self):
        """Override this method to initialize our application."""
        self.flake8 = app.Application()
        self.flake8.initialize([])
        options = self.flake8.option_manager.options
        for option in options:
            if option.parse_from_config:
                setattr(self, option.config_name, UNSET)

    def finalize_options(self):
        """Override this to parse the parameters."""
        options = self.flake8.option_manager.options
        for option in options:
            if option.parse_from_config:
                name = option.config_name
                value = getattr(self, name, UNSET)
                if value is UNSET:
                    pass
                else:
                    setattr(self.flake8.options, name, option.normalize_from_setuptools(value))

    def package_files(self):
        """Collect the files/dirs included in the registered modules."""
        seen_package_directories = ()
        directories = self.distribution.package_dir or {}
        empty_directory_exists = '' in directories
        packages = self.distribution.packages or []
        for package in packages:
            package_directory = package
            if package in directories:
                package_directory = directories[package]
            else:
                if empty_directory_exists:
                    package_directory = os.path.join(directories[''], package_directory)
            if package_directory.startswith(seen_package_directories):
                pass
            else:
                seen_package_directories += (package_directory + '.',)
                yield package_directory

    def module_files(self):
        """Collect the files listed as py_modules."""
        modules = self.distribution.py_modules or []
        filename_from = '{0}.py'.format
        for module in modules:
            yield filename_from(module)

    def distribution_files(self):
        """Collect package and module files."""
        for package in self.package_files():
            yield package

        for module in self.module_files():
            yield module

        yield 'setup.py'

    def run(self):
        """Run the Flake8 application."""
        self.flake8.run_checks(list(self.distribution_files()))
        self.flake8.formatter.start()
        self.flake8.report_errors()
        self.flake8.report_statistics()
        self.flake8.report_benchmarks()
        self.flake8.formatter.stop()
        try:
            self.flake8.exit()
        except SystemExit as e:
            if e.code:
                raise