# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/setup.py
# Compiled at: 2013-07-30 07:31:24
import glob, os, re, shutil, subprocess, sys
from distutils.core import Command

class PEP257Command(Command):
    description = 'Run pep257 with custom options'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call('find rapport -type f -name "*.py" | xargs pep257', shell=True)


class CleanupCommand(Command):
    patterns = [
     '.coverage', '.tox', '.venv', 'build', 'dist', '*.egg', '*.egg-info']
    description = 'Clean up project directory'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for pattern in CleanupCommand.patterns:
            for f in glob.glob(pattern):
                if os.path.isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.remove(f)


def get_cmdclass():
    """Dictionary of all distutils commands defined in this module.
    """
    return {'cleanup': CleanupCommand, 'pep257': PEP257Command}


def parse_requirements(requirements_file='requirements.txt'):
    requirements = []
    with open(requirements_file, 'r') as (f):
        for line in f:
            if re.match('\\s*-e\\s+', line):
                requirements.append(re.sub('\\s*-e\\s+.*#egg=(.*)$', '\\1', line))
            elif re.match('\\s*https?:', line):
                requirements.append(re.sub('\\s*https?:.*#egg=(.*)$', '\\1', line))
            elif re.match('\\s*-f\\s+', line):
                pass
            elif re.match('\\s*-r\\s+', line):
                pass
            elif line == 'argparse' and sys.version_info >= (2, 7):
                pass
            else:
                requirements.append(line.strip())

    return requirements