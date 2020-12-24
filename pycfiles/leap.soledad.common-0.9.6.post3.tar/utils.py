# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/drebs/dev/leap/repos/soledad/common/pkg/utils.py
# Compiled at: 2017-10-06 08:21:39
"""
Utils to help in the setup process
"""
import os, re, sys

def is_develop_mode():
    """
    Returns True if we're calling the setup script using the argument for
    setuptools development mode.

    This avoids messing up with dependency pinning and order, the
    responsibility of installing the leap dependencies is left to the
    developer.
    """
    args = sys.argv
    devflags = ('setup.py', 'develop')
    if (args[0], args[1]) == devflags:
        return True
    return False


def get_reqs_from_files(reqfiles):
    """
    Returns the contents of the top requirement file listed as a
    string list with the lines.

    @param reqfiles: requirement files to parse
    @type reqfiles: list of str
    """
    for reqfile in reqfiles:
        if os.path.isfile(reqfile):
            return open(reqfile, 'r').read().split('\n')


def parse_requirements(reqfiles=['requirements.txt',
 'requirements.pip',
 'pkg/requirements.pip']):
    """
    Parses the requirement files provided.

    The passed reqfiles list is a list of possible locations to try, the
    function will return the contents of the first path found.

    Checks the value of LEAP_VENV_SKIP_PYSIDE to see if it should
    return PySide as a dep or not. Don't set, or set to 0 if you want
    to install it through pip.

    @param reqfiles: requirement files to parse
    @type reqfiles: list of str
    """
    requirements = []
    skip_pyside = os.getenv('LEAP_VENV_SKIP_PYSIDE', '0') != '0'
    for line in get_reqs_from_files(reqfiles):
        if re.match('\\s*-e\\s+', line):
            pass
        elif re.match('\\s*https?:', line):
            requirements.append(re.sub('\\s*https?:.*#egg=(.*)$', '\\1', line))
        elif re.match('\\s*-f\\s+', line):
            pass
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        elif line == 'PySide' and skip_pyside:
            pass
        elif line.lstrip().startswith('#'):
            pass
        elif line != '':
            requirements.append(line)

    return requirements