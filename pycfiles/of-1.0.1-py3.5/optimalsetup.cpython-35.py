# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/tools/setup/optimalsetup.py
# Compiled at: 2016-11-22 11:24:38
# Size of source mod 2**32: 7840 bytes
"""
    ************
    Optimal Setup
    ************
    
    Optimal setup is an application that provides setup services for the Optimal framework.
    
    :copyright: Copyright 2010-2015 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details.
"""
import sys
from subprocess import CalledProcessError
__version__ = '0.9'
__release__ = '0.9.0'
__copyright__ = '2010-2016, Nicklas Boerjesson'
import os, json, getopt
major, minor, micro, releaselevel, serial = sys.version_info

def check_prerequisites():
    if major == 2:
        raise Exception('\nERROR RUNNING INSTALLATION:\nYou are running the setup with Python ' + str(major) + '.' + str(minor) + '.' + str(micro) + '!\nPlease install Python version 3.4 or higher and run with that version instead (python3 optimalsetup.py)')
    if major == 3 and minor < 4:
        _pythonversion = str(major) + '.' + str(minor) + '.' + str(micro)
        try:
            print('Python ' + _pythonversion + ' found, so checking if pip is installed..')
            import pip
            print('it was, continuing..')
        except ImportError:
            print("it wasn't, checking if easy_install is installed..")
            try:
                from setuptools.command import easy_install
                if minor == 3:
                    print('it was, installing pip..')
                    easy_install.main(['pip'])
                else:
                    print("it was, installing pip 7.1.2 because 8.x isn't compatible with 3.0-3.2..")
                    easy_install.main(['pip==7.1.2'])
            except ImportError:
                print("it wasn't, halting installation, raising error.")
                raise Exception('Error RUNNING INSTALLATION:\nYou are running the setup with Python ' + _pythonversion + "!\nIt doesn't have pip package management installed as default and this installation failed to install it automatically.\nPLease check the pip web site for instructions for your platform:\nhttps://pip.pypa.io/en/stable/installing/")


def install_package(_package_name, _arguments=None):
    """
    Install the packages listed if not present
    :param _package_name: The package to install
    :param _argument: An optional argument
    :return:
    """
    _installed = []
    import pip
    _exists = None
    if minor < 3:
        import pkgutil
        _exists = pkgutil.find_loader(_package_name)
    else:
        if minor == 3:
            import importlib
            _exists = importlib.find_loader(_package_name)
        else:
            import importlib
            _exists = importlib.util.find_spec(_package_name)
    if _exists is None:
        print(_package_name + ' not installed, installing...')
        if _arguments is None:
            pip.main(['install', _package_name])
        else:
            pip.main(['install', _package_name] + _arguments)
        print(_package_name + ' installed...')
        return True
    else:
        print(_package_name + ' already installed, skipping...')
        return False


sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
_help_msg = '\nUsage: optimal_setup.py [OPTION]... -d [DEFINITION FILE]... -l [LOG LEVEL]\nSet up and alter the Optimal Framework\n\nThis stand-alone tool facilitates setting up an installation of the framework\n\n    -d, --definitionfile    Provide the path to an JSON definition file to describe the setup\n    -e,                     Initialize editor\n    -l, --log_level         Log level\n    --default_of_install     Make a default Optimal Framework installation with the admin interface\n    \n    --help     display this help and exit\n    --version  output version information and exit\n\nAlways back up your data!\n\n'

def main():
    """Main program function"""
    _setup_filename = None
    _edit = None
    _log_level = None
    _default_of_install = None
    try:
        _opts = None
        _args = None
        _opts, _args = getopt.getopt(sys.argv[1:], 'ed:l:', ['help', 'version', 'default_of_install', 'definitionfile=*.json', 'log_level='])
    except getopt.GetoptError as err:
        print(str(err) + '\n' + _help_msg + '\n Arguments: ' + str(_args))
        sys.exit(2)

    if _opts:
        for _opt, _arg in _opts:
            if _opt == '-e':
                _edit = True
            elif _opt in ('-d', '--definitionfile'):
                _setup_filename = _arg
            elif _opt in ('-l', '--log_level'):
                _log_level = _arg
            else:
                if _opt == '--help':
                    print(_help_msg)
                    sys.exit()
                else:
                    if _opt == '--version':
                        print(__version__)
                        sys.exit()
                    elif _opt == '--default_of_install':
                        _default_of_install = True

        check_prerequisites()
        install_package('dulwich', ['--global-option=--pure'])
        install_package('distlib')
        install_package('of', '--upgrade')
        from of.tools.setup.lib.setup import Setup
        if sys.platform == 'windows':
            install_package('win32api')
        if _default_of_install:
            print('Selecting the default installation')
            _setup = Setup(_default_of_install=_default_of_install)
    elif _setup_filename:
        print('Load setup file: ' + _setup_filename)
        with open(_setup_filename, 'r') as (f):
            _setup = Setup(_setup_filename=_setup_filename)
    else:
        _setup = Setup()
    if _log_level:
        _setup.log_level = int(_log_level)
    if not _edit and _default_of_install:
        _log = _setup.install()
    else:
        if _edit or not _setup_filename:
            if sys.platform == 'linux':
                try:
                    import _tkinter
                except ImportError:
                    print('On Linux, the python3-tk package has to be installed:')
                    print('----------------python3-tk installing----------------------------------')
                    from subprocess import check_call
                    try:
                        check_call(['sudo', 'apt-get', 'install', 'python3-tk', '--yes'])
                        print('----------------python3-tk installed----------------------------------')
                    except CalledProcessError:
                        print('Failed to install the python3-tk-package. Please run "sudo apt-get install python3-tk" manually.')
                        exit(1)

                from of.tools.setup.lib.main_tk_setup import SetupMain
                SetupMain(_setup=_setup, _setup_filename=_setup_filename)
            else:
                _log = _setup.install()
            print(str(_log))
        else:
            print('Error: No options provided.\n' + _help_msg)


if __name__ == '__main__':
    main()