# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/domdfcoding/msp2lib/msp2lib/core.py
# Compiled at: 2020-04-26 17:39:03
# Size of source mod 2**32: 5726 bytes
"""
Convert an MSP file representing one or more Mass Spectra to a NIST MS Search user library.

Docker must be installed to use this program.

The first time this script is run it will download the latest
version of the docker image automatically.

This can also be done manually, such as to upgrade to the latest version,
by running with the ``--get-docker-image`` flag.
"""
import os, pathlib, shutil, sys, tempfile
from .utils import _ask_existing_lib, _prep_workdirs, about, build_docker_image, download_docker_image, test_docker, version

def msp2lib(msp_file, output_dir, lib_name=None):
    """
        Convert the provided MSP file to a NIST User Library, and store the newly
        created library in the given output directory.
        
        :param msp_file: The MSP file to convert to a NIST User Library
        :type msp_file: str or pathlib.Path
        :param output_dir: The directory to store the NIST User Library in
        :type output_dir: str or pathlib.Path
        :param lib_name: The name of the NIST User Library. If ``None`` this will
                be the filename of the MSP file without the extension.
        :type lib_name: str, optional
        """
    msp_file = pathlib.Path(msp_file)
    if lib_name is None:
        lib_name = msp_file.stem
    with tempfile.TemporaryDirectory() as (workdir):
        input_workdir, output_workdir = _prep_workdirs(workdir)
        shutil.copy(msp_file, input_workdir / 'input.msp')
        _run_docker(input_workdir, output_workdir)
        shutil.copytree(output_workdir / 'input', output_dir / lib_name)


def _run_docker(input_dir, output_dir):
    """
        Launch the docker container.
        
        :param input_dir: The path to the directory containing the input MSP file.
                The input MSP file MUST be named `input.msp`
        :type input_dir: str or pathlib.Path
        :param output_dir: The path to the directory where docker will save the created library.
                The new library will be named `input`, but can be renamed after creation.
        :type output_dir: str or pathlib.Path
        
        On Unix, the return value is the exit status of the process encoded in the
        format specified for :fun:`python:os.wait()`. Note that POSIX does not specify
        the meaning of the return value of the C system() function, so the return value
        is system-dependent.

        On Windows, the return value is that returned by the system shell after running command.
        The shell is given by the Windows environment variable COMSPEC: it is usually cmd.exe,
        which returns the exit status of the command run; on systems using a non-native shell,
        consult your shell documentation.
        """
    return os.system(f"docker run --name=lib2nist-wine --rm -v '{input_dir}:/input' -v '{output_dir}:/output' --env USER_UID={os.getuid()} domdfcoding/lib2nist-wine /make_nistlib.sh")


def main():
    """
        Entry point for running from the command line.
        """
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_file', help='The MSP file to convert.', nargs='?')
    parser.add_argument('output_dir', help='The directory to save the output library in.', nargs='?')
    parser.add_argument('--version',
      dest='version', action='store_true', default=False, help='Show the version number and exit.')
    parser.add_argument('--get-docker-image',
      dest='get_image', action='store_true', default=False, help='Download the docker image now rather than at first run, then exit.')
    parser.add_argument('--build-docker-image',
      dest='build_image', action='store_true', default=False, help='Build the docker image from the Dockerfile, then exit.')
    args = parser.parse_args()
    if args.version:
        version()
        sys.exit(0)
    elif not test_docker():
        parser.error('Docker installation not found. Please install Docker and try again.\nSee https://docs.docker.com/get-docker/ for more information.')
    else:
        if args.get_image:
            sys.exit(download_docker_image())
        else:
            if args.build_image:
                sys.exit(build_docker_image())
            else:
                if args.input_file:
                    about()
                    input_file = pathlib.Path(args.input_file).absolute()
                    lib_name = input_file.stem
                    if not input_file.is_file():
                        parser.error(f"Input file not found at the given path: {input_file}")
                    if args.output_dir:
                        output_dir = pathlib.Path(args.output_dir).absolute()
                    else:
                        output_dir = pathlib.Path.cwd().absolute()
                    if not output_dir.is_dir():
                        output_dir.mkdir(parents=True)
                    output_lib_dir = output_dir / lib_name
                    if output_lib_dir.exists():
                        if _ask_existing_lib(lib_name):
                            shutil.rmtree(output_lib_dir)
                        else:
                            sys.exit(0)
                    msp2lib(input_file, output_dir, lib_name)
                else:
                    parser.error('Please specify an input file.')