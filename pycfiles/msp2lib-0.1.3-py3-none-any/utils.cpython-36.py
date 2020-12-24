# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/domdfcoding/msp2lib/msp2lib/utils.py
# Compiled at: 2020-04-26 17:39:03
# Size of source mod 2**32: 3880 bytes
"""
utilities for msp2lib
"""
import distutils.spawn, pathlib, re, subprocess
from msp2lib import __copyright__, __version__

def test_docker():
    """
        Returns whether Docker is installed on the system
        
        :return: ``True`` if Docker is installed, ``False`` otherwise.
        :rtype: bool
        """
    return bool(distutils.spawn.find_executable('docker'))


def version():
    """
        Prints the version number of msp2lib
        """
    print(__version__)


def about():
    """
        Prints information about msp2lib
        """
    print(f"msp2lib Version {__version__} Copyright (C) {__copyright__}\nThis program comes with ABSOLUTELY NO WARRANTY, to the extent permitted by law.\nThis is free software: you are free to change and redistribute it under certain conditions.\nSee https://www.gnu.org/licenses/lgpl-3.0.en.html for more information.")


def _prep_workdirs(workdir):
    """
        Prepare input and output directories in the given directory.
        These will be then mounted in the docker container.
        
        :param workdir:
        :type workdir: str or pathlib.Path
        :return: The newly created directories
        :rtype: pathlib.Path, pathlib.Path
        """
    workdir = pathlib.Path(workdir)
    input_workdir = workdir / 'input'
    input_workdir.mkdir(parents=True)
    output_workdir = workdir / 'output'
    output_workdir.mkdir(parents=True)
    return (
     input_workdir, output_workdir)


def _ask_existing_lib(lib_name):
    """
        Asks the user whether they wish to remove an existing library that exists with the same name.
        
        :param lib_name: The name of the library that already exists
        :type lib_name: str
        
        :return: ``True`` if the responded with ``y`` to indicate they wish to remove
                the existing library, ``False`` otherwise.
        :rtype: bool
        """
    print(f"\nA library already exists in the output location with the name '{lib_name}'.")
    return input('Do you want to remove the existing library? [y/N] ').lower().startswith('y')


def download_docker_image():
    """
        Pull the lib2nist-wine docker image from dockerhub.
        
        :return: The return code of the ``docker pull`` command
        :rtype: int
        """
    process = subprocess_with_log('docker pull domdfcoding/lib2nist-wine')
    return int(process.returncode)


def build_docker_image():
    """
        Build the lib2nist-wine docker image from the Dockerfile.

        :return: The return code of the ``docker build`` command
        :rtype: int
        """
    pkg_dir = pathlib.Path(__file__).parent.absolute()
    process = subprocess_with_log(f"docker build --no-cache -t domdfcoding/lib2nist-wine {pkg_dir}/.")
    return int(process.returncode)


def subprocess_with_log(command):
    """
        The ``command`` with :class:`python:subprocess.Popen`, printing any stdout from the command.
        
        :param command: The command to run
        :type command: str or list of str
        
        :return:
        :rtype: :class:`python:subprocess.Popen`
        """
    process = subprocess.Popen(command, stdout=(subprocess.PIPE), shell=True)
    for line in iter(process.stdout.readline, b''):
        print(re.sub('\\n$', '', line.decode('UTF-8')))

    return process