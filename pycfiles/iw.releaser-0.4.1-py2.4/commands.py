# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/commands.py
# Compiled at: 2008-04-29 08:14:25
""" releaser
"""
import sys, os, re
from os.path import join
from fnmatch import fnmatch
from setuptools import Command
from ConfigParser import ConfigParser
from iw.releaser.base import yes_no_input
from iw.releaser.base import safe_input
from iw.releaser.base import display
from iw.releaser.packet import get_version
from iw.releaser.packet import get_name
from iw.releaser.packet import raise_version
from iw.releaser.packet import check_tests
from iw.releaser.packet import increment_changes
from iw.releaser.packet import create_branches
from iw.releaser.packet import pypi_upload
from iw.releaser.hook import apply_hooks
from msgfmt import Msgfmt
ROOT_FILE = join(os.path.expanduser('~'), '.pypirc')
ROOT_FILE_2 = join(os.path.expanduser('~'), 'pypirc')
CONF_FILE = 'iw-releaser.cfg'

class release(Command):
    """Releaser"""
    __module__ = __name__
    description = 'Releases an egg'
    user_options = [('testing', 't', 'run tests before anything'), ('release', 'r', 'release package'), ('upload', 'u', 'upload package'), ('version=', None, 'new version number'), ('auto', 'a', 'automatic mode')]

    def initialize_options(self):
        """init options"""
        self.testing = False
        self.release = False
        self.upload = False
        self.version = ''
        self.auto = False

    def finalize_options(self):
        """finalize options"""
        if self.auto and not self.version:
            display('You must specify a version in auto mode')
            sys.argv.append('-h')
            __import__('setup')
            sys.exit(-1)

    def run(self):
        """runner"""
        make_package_release(auto=self.auto, testing=self.testing, release=self.release, upload=self.upload, new_version=self.version)


def _get_commands(conf, package_name):
    """Reads a conf file and extract the commands to run"""
    parser = ConfigParser()
    parser.read(conf)

    def _validate_command(cmd, package):
        command = 'mregister sdist bdist_egg mupload'
        packages = []
        for option in ('packages', 'release-packages'):
            if option in parser.options(cmd):
                packages = parser.get(cmd, option).split('\n')
                break

        for option in ('command', 'release-command'):
            if option in parser.options(cmd):
                command = parser.get(cmd, option)
                break

        exprs = [ r.strip() for r in packages ]
        for expr in exprs:
            founded = [ r for r in re.findall(expr, package) if r.strip() != '' ]
            if founded != []:
                return '%s -r %s' % (command, cmd)

        return

    commands = []
    if 'release' in parser.sections():
        if 'commands' in parser.options('release'):
            commands = parser.get('release', 'commands').split('\n')
    elif 'distutils' in parser.sections():
        if 'index-servers' in parser.options('distutils'):
            commands = parser.get('distutils', 'index-servers').split('\n')
    commands = [ cmd.strip() for cmd in commands if cmd.strip() != '' ]
    res = [ _validate_command(cmd, package_name) for cmd in commands ]
    return [ r for r in res if r is not None ]


def make_package_release(auto=False, testing=False, release=False, upload=False, new_version=''):
    """release process"""
    version = get_version()
    display('This package is version %s' % version)
    package_name = get_name()
    places = (
     join(os.path.expanduser('~'), CONF_FILE), join(os.getcwd(), CONF_FILE))
    commands = []
    for place in places:
        if os.path.exists(place):
            commands = _get_commands(place, package_name)
            break

    if commands == []:
        for place in (ROOT_FILE, ROOT_FILE_2):
            if os.path.exists(place):
                commands = _get_commands(place, package_name)

    if not auto:
        if not testing:
            testing = yes_no_input('Do you want to run tests before releasing ?', default='n')
        if testing:
            check_tests()
    if not auto:
        if not release:
            release = yes_no_input('Do you want to create the release ? If no, you will just be able to deploy again the current release')
    else:
        release = True
    if release:
        if not auto:
            if not new_version:
                new_version = safe_input('Enter a version', version)
            if version != new_version:
                raise_version(new_version)
        else:
            if not new_version:
                new_version = str(float(version) + 0.1)
            display('Raising the version...')
            raise_version(new_version)
        display('Commiting changes...')
        increment_changes()
        display('Creating branches...')
        create_branches()
    else:
        new_version = version
    if commands != []:
        pypi_upload(commands)
        display('%s released' % new_version)
        apply_hooks(package_name=package_name, version=new_version)


class build_mo(Command):
    """Msgfmt"""
    __module__ = __name__
    description = 'Build msgfmt .mo files from their .po sources'
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        self.find_locales(os.getcwd())

    def find_locales(self, path):
        """find 'locales' directories and compiles .po files
        """
        for directory in os.listdir(path):
            dir_path = join(path, directory)
            if not os.path.isdir(dir_path):
                continue
            if directory == 'locales':
                self.compile_po(dir_path)
            else:
                self.find_locales(dir_path)

    def compile_po(self, path):
        """path is a locales directory, find ??/LC_MESSAGES/*.po and compiles
        them into .mo
        """
        for language in os.listdir(path):
            lc_path = join(path, language, 'LC_MESSAGES')
            if os.path.isdir(lc_path):
                for domain_file in os.listdir(lc_path):
                    if domain_file.endswith('.po'):
                        file_path = join(lc_path, domain_file)
                        display('Building .mo for %s' % file_path)
                        mo_file = join(lc_path, '%s.mo' % domain_file[:-3])
                        mo_content = Msgfmt(file_path, name=file_path).get()
                        mo = open(mo_file, 'wb')
                        mo.write(mo_content)
                        mo.close()