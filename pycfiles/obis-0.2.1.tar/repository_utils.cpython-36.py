# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vermeul/openbis/obis/src/python/obis/dm/repository_utils.py
# Compiled at: 2018-07-10 03:51:00
# Size of source mod 2**32: 1271 bytes
import os, socket
from .commands.openbis_command import CommandResult
from .utils import run_shell

def copy_repository(ssh_user, host, path):
    repository_folder = path.split('/')[(-1)]
    if os.path.exists(repository_folder):
        return CommandResult(returncode=(-1), output=('Folder for repository to clone already exists: ' + repository_folder))
    else:
        location = get_repository_location(ssh_user, host, path)
        return run_shell(['rsync', '--progress', '-av', location, '.'])


def delete_repository(ssh_user, host, path):
    if is_local(host):
        result = run_shell(['chmod', '-R', 'u+w', path])
        if result.failure():
            return result
        return run_shell(['rm', '-rf', path])
    else:
        location = ssh_user + '@' if ssh_user is not None else ''
        location += host
        return run_shell(['ssh', location, 'rm -rf ' + path])


def is_local(host):
    return host == socket.gethostname()


def get_repository_location(ssh_user, host, path):
    if is_local(host):
        location = path
    else:
        location = ssh_user + '@' if ssh_user is not None else ''
        location += host + ':' + path
    return location