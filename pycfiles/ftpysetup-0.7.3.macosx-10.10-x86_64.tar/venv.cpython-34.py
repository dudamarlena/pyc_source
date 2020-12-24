# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/venv/venv.py
# Compiled at: 2015-01-01 14:50:17
# Size of source mod 2**32: 4233 bytes
"""Setup and activate a python virtual environment through setup."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
__all__ = [
 'VirtualEnv']
import sys
if sys.version_info < (3, 3):
    raise Exception('venv requires Python 3.3 or higher.')
import os, re, venv, ensurepip, subprocess, setuptools

class EnvBuilder(venv.EnvBuilder):

    def ensure_directories(self, env_dir):
        context = super().ensure_directories(env_dir)
        if os.path.islink(context.executable):
            real = os.path.realpath(context.executable)
            dirname, exename = os.path.split(os.path.abspath(real))
            context.executable = real
            context.python_dir = dirname
            context.python_exe = exename
            context.env_exe = os.path.join(context.bin_path, exename)
        return context


class VirtualEnv(setuptools.Command):
    description = 'Setup the venv for this project.'
    user_options = [
     ('venv-base=', None, 'path to virtual environment directory (default: VENV)'),
     ('upgrade', 'U', 'upgrade the packages')]

    def initialize_options(self):
        self.venv_base = None
        self.upgrade = False

    def finalize_options(self):
        if self.venv_base is None:
            self.venv_base = 'VENV'
        self.venv_base = os.path.abspath(self.venv_base)
        self.activate_path = os.path.join(self.venv_base, 'bin', 'activate')

    def run(self):
        try:
            venvbuild = EnvBuilder(system_site_packages=False, clear=False, symlinks=True, upgrade=False, with_pip=True)
            venvbuild.create(self.venv_base)
        except Exception as err:
            print('Error: {0}'.format(err), file=sys.stderr)
            return

        env_re = re.compile('^(?P<key>\\w+)=(?P<value>.*)$')
        env_args = ['/bin/bash', '--posix']
        env_input = ['. {0.activate_path}'.format(self), 'set']
        env = subprocess.check_output(env_args, input=bytes('\n'.join(env_input), 'utf8'))
        env = [env_re.match(x) for x in str(env, 'utf-8').split()]
        env = [(m.group('key'), m.group('value')) for m in env if m]
        env = dict(env)
        keys = list(env.keys())
        keys.sort()

        def process_requires(name):
            value = getattr(self.distribution, name, [])
            if value is None:
                return
            if not isinstance(value, list):
                value = [
                 value]
            for package in value:
                self.install_package(package, env)

        process_requires('setup_requires')
        process_requires('install_requires')
        process_requires('tests_require')
        print()
        print('Activate with: . {0}'.format(os.path.relpath(self.activate_path)))

    def install_package(self, package, env):
        args = []
        args.append(os.path.join(self.venv_base, 'bin', 'pip'))
        args.append('install')
        if self.upgrade:
            args.append('--upgrade')
        args.append(package)
        subprocess.check_call(args, env=env, stdout=sys.stdout, stderr=sys.stderr)