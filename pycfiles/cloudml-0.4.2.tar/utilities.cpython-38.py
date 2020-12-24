# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudmitigator_semantic/utilities.py
# Compiled at: 2020-03-26 22:21:52
# Size of source mod 2**32: 957 bytes
__doc__ = 'Handle interaction with bash.'
import subprocess

def run_bash_command_return_error(command):
    """Convert command into bash command."""
    command = command.split(' ')
    try:
        bash_return = subprocess.run(command, capture_output=True, check=True)
    except Exception as error:
        try:
            raise TypeError(f"Bash command did not execute properly \n command: {command} \n error: {error}")
        finally:
            error = None
            del error

    else:
        return bash_return.stdout.decode('utf-8')


def run_bash_command_split_lines_return_error(command):
    """Convert command into bash command split lines."""
    command = command.split(' ')
    try:
        bash_return = subprocess.run(command, capture_output=True, check=True)
    except Exception as error:
        try:
            raise TypeError(f"Bash command did not execute properly \n command: {command} \n error: {error}")
        finally:
            error = None
            del error

    else:
        return bash_return.stdout.decode('utf-8').splitlines()