# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.dennis/development/ship_it/ship_it/virtualenv.py
# Compiled at: 2018-07-05 16:56:37
from __future__ import unicode_literals
import logging, sys
from os import path
from pipes import quote
import invoke
logger = logging.getLogger(__name__)

def _quote_and_vlidate_file(filepath):
    """
    Checking that the file exists, is absolute, and is a file.
    Return quoted file

    :param filepath: path to file
    """
    assert path.isabs(filepath) and path.isfile(filepath)
    return quote(filepath)


def _quote_and_validate_dir(dirpath):
    """
    Checking that the directory exists and is absolute
    Return quoted directory

    :param dirpath: path to directory
    """
    assert path.isabs(dirpath)
    return quote(dirpath)


def get_virtualenv():
    assert sys.executable, b"can't infer python executable path"
    return (b'{} -m virtualenv').format(quote(sys.executable))


class VirtualEnvPackager(object):

    def __init__(self, virtualenv_path, upgrade_pip=False, upgrade_wheel=False):
        """
        :param virtualenv_path: the path to the virtualenv we're going to make
        :param upgrade_pip: upgrade pip after building virtualenv
        :param upgrade_wheel: upgrade wheel after building virtualenv
        """
        self.virtualenv_path = virtualenv_path
        self.build_virtualenv(virtualenv_path, upgrade_pip, upgrade_wheel)

    def build_virtualenv(self, virtualenv_path, upgrade_pip, upgrade_wheel):
        """
        :param virtualenv_path: the path to the virtualenv we're going to make
        :param upgrade_pip: upgrade pip after building virtualenv
        :param upgrade_wheel: upgrade wheel after building virtualenv
        """
        quoted_path = _quote_and_validate_dir(virtualenv_path)
        if path.exists(virtualenv_path):
            invoke.run((b'rm -rf {}').format(quoted_path))
        invoke.run((b'{virtualenv} {location}').format(virtualenv=get_virtualenv(), location=quoted_path))
        if upgrade_pip:
            invoke.run((b'{pip} install --upgrade pip').format(pip=quote(path.join(virtualenv_path, b'bin', b'pip'))))
        if upgrade_wheel:
            invoke.run((b'{pip} install --upgrade wheel').format(pip=quote(path.join(virtualenv_path, b'bin', b'pip'))))

    def run_venv_command(self, command, arg_list):
        """
        Run a command in virtualenv's /bin/ folder

        :param command: the command to run
        :param arg_list: list of arguments passed to command
        """
        args = (b' ').join(arg_list)
        command = quote(path.join(self.virtualenv_path, b'bin', command))
        invoke.run((b'{command} {args}').format(command=command, args=args))

    def install_package(self, setup_py_path):
        """
        Run python setup.py install

        :param setup_py_path: the path to setup.py
        """
        setup_file = _quote_and_vlidate_file(setup_py_path)
        self.run_venv_command(b'python', [setup_file, b'install'])

    def install_requirements(self, requirements_file_path):
        """
        Package installation is provided by requirements file. Usually
        because '.' is included in requirements file.

        :param requirements_file_path: the path to the requirements.txt file
        """
        req_file = _quote_and_vlidate_file(requirements_file_path)
        self.run_venv_command(b'pip', [b'install', b'-r', req_file])

    def pip_install_package(self, requirements_file_path):
        """
        Install local package from '.' using pip. Installs requirements from
        requirements_file_path first.

        :param requirements_file_path: the path to the requirements.txt file
        """
        self.install_requirements(requirements_file_path)
        self.run_venv_command(b'pip', [b'install', b'.'])

    def copy_package(self, requirements_file_path, package_path):
        """
        :param requirements_file_path: the path to the requirements.txt file
        :param package_path: the path to the package we're going to copy into
            the virtualenv
        """
        req_file = _quote_and_vlidate_file(requirements_file_path)
        pkg_path = _quote_and_validate_dir(package_path)
        self.run_venv_command(b'pip', [b'install', b'-r', req_file])
        invoke.run((b'find {pkg} -type f -name "*.py[co]" -delete;find {pkg} -type d -name "__pycache__" -delete').format(pkg=pkg_path))
        invoke.run((b'cp -r {} {}').format(quote(package_path.rstrip(b'/')), quote(self.virtualenv_path)))

    def patch_virtualenv(self, destination_path):
        """
        Patch the virtualenv we built to be relocatable and

        :param destination_path: the path you expect it to be in the resulting
            system
        """
        self.remove_prelink_if_applicable()
        invoke.run((b'{virtualenv} --relocatable {local_path}').format(virtualenv=get_virtualenv(), local_path=quote(self.virtualenv_path)))
        invoke.run((b'sed -i "s:{local}:{dest}:" {local_activate}').format(local=self.virtualenv_path, dest=destination_path, local_activate=quote(path.join(self.virtualenv_path, b'bin', b'activate'))))

    def remove_prelink_if_applicable(self):
        """
        Packaging a virtualenv has issues if you prelink the executables. Ideally,
        Prelink would be uninstalled on the system, but if it is, we need to undo
        it for our python.
        """
        try:
            invoke.run((b'prelink -u {}').format(quote(path.join(self.virtualenv_path, b'bin', b'python'))))
        except:
            logger.debug(b'prelink not undone due to error', exc_info=True)