# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/virtual.py
# Compiled at: 2012-08-01 04:26:16
"""Interface to `virtualenv <http://www.virtualenv.org/>`_.

The main purpose is to support running the build in:

    * An existing virtual environment
    * A new virtual environment
    * A freshly recreated virtual environment"""
from dovetail.util import InvalidEnvironment, Logger
from dovetail.util.which import which
from sys import executable, modules
import subprocess, os
from tempfile import mkdtemp
from shutil import rmtree
RETURN_CODE = 170
PYTHON_TEST = ('\n# Simple sanity test that we are running in a Python environment\ndef f():\n    exit({0})\nf()\n').format(RETURN_CODE)

def probe_existing(directory, python_exe):
    """Validates the virtual environment to ensure it can be used,
    raising an exception if it is not.

    :param directory: A path to the virtual environment to be tested
    :type  directory: string
    :param python_exe: A path to the Python executable in the environment
    :type  python_exe: string
    :raises: :exc:`.InvalidEnvironment`
    """
    if not os.path.isdir(directory):
        raise InvalidEnvironment(('Virtual Environment {0} is not a directory').format(directory))
    if not os.access(directory, os.R_OK):
        raise InvalidEnvironment(('Cannot read Virtual Environment directory {0}').format(directory))
    if not os.path.isfile(python_exe):
        raise InvalidEnvironment(('Virtual Environment {0} does not appear valid - missing Python executable {1}').format(directory, python_exe))
    if not os.access(python_exe, os.R_OK | os.X_OK):
        raise InvalidEnvironment(('Invalid read and/or execute permission on Python runtime {0}').format(python_exe))
    if not os.access(directory, os.W_OK):
        Logger.warn(('Cannot write into Virtual Environment {0}: Might not be able to install package requirements.').format(directory))
    result = subprocess.call([python_exe, '-c', PYTHON_TEST])
    if result != RETURN_CODE:
        raise InvalidEnvironment(('Executable does not appear to be a working Python interpreter: {0}').format(python_exe))
    Logger.debug('Virtual environment seems OK')


def probe_new(directory, python_exe):
    """Validates whether we can create a virtual environment - can we write to
    the specified directory?

    :param directory: A path to the virtual environment to be tested
    :type  directory: string
    :param python_exe: A path to the Python executable in the environment
    :type  python_exe: string
    :raises: :exc:`.InvalidEnvironment`
    """
    parent = os.path.dirname(directory)
    if not os.access(parent, os.W_OK):
        raise InvalidEnvironment(('Cannot create virtual environment: No write permission to {0}').format(parent))
    if os.path.isdir(directory):
        if not os.access(directory, os.W_OK):
            raise InvalidEnvironment(('Cannot clear old virtual environment: No write permission to {0}').format(directory))
        if not os.path.isfile(python_exe) or not os.access(python_exe, os.X_OK):
            raise InvalidEnvironment(('Cowardly refusing to wipe directory. {0} does not look like a virtual environment - Python is missing/not executable.\nPlease manually delete this directory, or manually run virtualenv to proceed.').format(directory))
        Logger.debug(('Iterating files and directories under {0} to check file permissions').format(directory))
        for dir_path, dir_names, file_names in os.walk(directory):
            items = dir_names
            items.extend(file_names)
            for item in items:
                file_name = os.path.join(dir_path, item)
                if not os.path.islink(file_name) and not os.access(file_name, os.W_OK):
                    rel = os.path.relpath(file_name, directory)
                    raise InvalidEnvironment(('Cannot clear old virtual environment: No write permission to {0}').format(rel))

    Logger.debug('File permissions suggest we can create a new virtual environment')


def install_virtualenv():
    """Attempts to install and validate virtualenv returning the path
    to the virtualenv executable.

    If the installation fails, the function raises :exc:`.InvalidEnvironment`
    exception.

    :return: The full path to the newly-created :program:`virtualenv` executable
    :rtype:  string
    :raises: :exc:`.InvalidEnvironment`
    """
    from dovetail.directives.packages import install
    install(['virtualenv'])
    try:
        import virtualenv
        program = 'virtualenv'
        if os.name == 'nt':
            program += '.exe'
        exe = which(program)
        if exe is None:
            raise InvalidEnvironment(('Installed virtualenv but cannot find the {0} on the system path.\nThis may be due to an nonsensical PATH or a corrupt environment. Try\nreinstalling virtualenv manually.').format(program))
        return exe
    except ImportError:
        raise InvalidEnvironment('Attempted to install virtualenv, but failed.\n This could be a caused by several conditions:\n  * You do not have file permission to install virtualenv to the current Python\n    environment\n  * Corrupted environment\n This is frequently solved by reinstalling virtualenv with appropriate\n permissions, eg running "easy_install virtualenv", or by recreating\n your virtual environment".')

    return


def get_virtualenv_command(directory, clear=False):
    """Returns the command to create a virtualenv environment.

    :param directory: A path to the virtual environment to be tested
    :type  directory: string
    :param clear: Erase any pre-existing environment?
    :type  clear: boolean
    :return: A command suitable for executing with :func:`subprocess.call`
    :rtype:  list of string
    """
    exe = install_virtualenv()
    command = [exe, directory]
    if clear:
        command.insert(1, '--clear')
    return command


def prepare_virtual(proposed, clear):
    """Prepare the proposed virtual environment, returning the path to the Python
    executable to use.

    This function will call :program:`virtualenv` to create the environment if either
    the environment is not present, or the --clear option was specified.

    :param proposed: A path to the virtual environment to be created or used
    :type  proposed: string
    :param clear: Erase any pre-existing environment?
    :type  clear: boolean
    :return: The full path to the :program:`virtualenv` executable under **proposed**
    :rtype:  string
    :raises: :exc:`.InvalidEnvironment`
    """
    if proposed is None:
        return
    else:
        absolute = os.path.abspath(proposed)
        if os.name == 'nt':
            python = os.path.join(absolute, 'Scripts', 'python.exe')
        else:
            python = os.path.join(absolute, 'bin', 'python')
        if os.path.dirname(python) == os.path.dirname(executable):
            if clear:
                raise InvalidEnvironment(('Cowardly refusing to recreate Virtual environment {0}: We are running in this environment now.').format(proposed))
            Logger.warn(('Virtual environment {0} has already been activated. Ignoring -e option.').format(proposed))
            return
        exists = os.path.isdir(absolute)
        if exists:
            Logger.debug(('Directory {0} exists. Probing...').format(proposed))
        create = False
        if clear:
            probe_new(absolute, python)
            create = True
        elif exists:
            probe_existing(absolute, python)
        else:
            probe_new(absolute, python)
            create = True
        if create:
            command = get_virtualenv_command(absolute, clear)
            if exists:
                Logger.major(("Found existing virtual environment '{0}'. Wiping and recreating.").format(proposed))
            else:
                Logger.major(("Creating new virtual environment '{0}'").format(proposed))
            Logger.log(('Running command: {0}').format((' ').join(command)))
            result = subprocess.call(command)
            if result:
                raise InvalidEnvironment(('Failed to create virtual environment {0}\n> {1}\n  returned error {2}').format(proposed, (' ').join(command), result))
            try:
                probe_existing(absolute, python)
                Logger.log(('Virtual environment {0} created successfully').format(proposed))
            except InvalidEnvironment as exception:
                raise InvalidEnvironment(('New virtual environment appears invalid: {0}').format(exception.message))

        else:
            Logger.major(("Reusing existing virtual environment '{0}'").format(proposed))
        return python


def find_self_on_sys_path():
    """Returns the :mod:`sys.path` entry that loaded this module (:mod:`dovetail`)

    :return: Path to :mod:`dovetail`
    :rtype:  string"""
    root = __name__.rpartition('.')[0]
    file_name = modules[root].__file__
    path_name = os.path.dirname(os.path.dirname(file_name))
    import sys
    assert path_name in sys.path
    return path_name


BOOTSTRAP = '\n# Check to see if Dovetail is running\nimport sys\nimport os\ntry:\n    import dovetail\n    print "Dovetail is already installed"\nexcept ImportError:\n    print "Dovetail is not installed in virtual environment. Modifying system path"\n    path = sys.argv[1]\n    sys.path.insert(0, path)\n    try:\n        import dovetail\n        print "Dovetail loaded from", path\n    except ImportError as exception:\n        print "Path", path, "did not work - got exception:", exception\n        print "Failing build"\n        exit(254)\n\nvirtualenv = os.path.dirname(os.path.dirname(sys.executable))\ndovetail.util.utilities.set_virtual_environment(virtualenv)\ndovetail.main.main(*sys.argv[2:])\n'

def write_bootstrap(directory):
    """Creates a bootstrap Python file in a directory, returning the
    path to the bootstrap file.

    :param directory: Path to directory in which to write the bootstrap
    :type  directory: string
    :return: Path to the **bootstrap.py** file
    :rtype:  string
    """
    file_name = os.path.join(directory, 'bootstrap.py')
    bootstrap = open(file_name, 'w')
    try:
        bootstrap.write(BOOTSTRAP)
    finally:
        bootstrap.close()

    return file_name


def build_command_line(python, bootstrap, arguments):
    """Produce a command line for calling a virtual environment.

    :param python:    Path to the Python executable in a virtual environment
    :type  python:    string
    :param bootstrap: Path to the **bootstrap.py** file which bootstraps the
                      build in the virtual environment
    :type  bootstrap: string
    :param arguments: Additional command line arguments
    :type  arguments: list of string
    :return: The command line to bootstrap the build in a virtual environment
    :rtype:  string

    This is basically the same as the command line which called this, but
    we remove the virtual environment arguments"""
    new = [
     python, bootstrap, find_self_on_sys_path()]
    skip = False
    for arg in arguments:
        if skip:
            skip = False
        elif arg == '--virtualenv' or arg == '-e':
            skip = True
        elif arg == '--clear':
            pass
        else:
            new.append(arg)

    return new


def run_virtual(virtualenv, clear, kw):
    """Runs the test in a virtualenv environment, creating and clearing it
    if necessary.

    :param virtualenv: A path to a existing or to-be-built virtual environment
    :type  virtualenv: string
    :param clear:      Erase any pre-existing environment?
    :type  clear:      boolean
    :param kw:         Command line arguments
    :type  kw:         list of string
    :return:           The return of the :func:`subprocess.call` process
    :rtype:            int

    The arguments from the original invocation should be passed untouched
    and will (after manipulation) be passed to the virtual environment
    """
    python = prepare_virtual(virtualenv, clear)
    if python:
        temp_dir = mkdtemp()
        try:
            bootstrap = write_bootstrap(temp_dir)
            Logger.debug(('Writing bootstrap script to {0}').format(bootstrap))
            command_line = build_command_line(python, bootstrap, kw)
            Logger.major(('Running build: {0}').format((' ').join(command_line)))
            return subprocess.call(command_line)
        finally:
            rmtree(temp_dir, ignore_errors=True)