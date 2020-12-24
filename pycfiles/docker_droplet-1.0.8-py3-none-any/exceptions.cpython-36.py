# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/docker-droplet/docker_droplet/exceptions.py
# Compiled at: 2020-02-14 12:38:23
# Size of source mod 2**32: 334 bytes


class PathNotResolvable(Exception):

    def __init__(self, name, value):
        msg = f"The provided path for {name}: '{value}' is not resolvable"
        super().__init__(msg)


class MissingVariable(Exception):

    def __init__(self, name):
        msg = f"Variable {name} is missing"
        super().__init__(msg)