# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/templ8/templ8/exceptions.py
# Compiled at: 2020-03-02 10:58:12
# Size of source mod 2**32: 443 bytes


class MissingConfig(Exception):

    def __init__(self, key):
        super().__init__(f"\nMissing config: {key} not found in config file")


class OutputDirInvalid(Exception):

    def __init__(self, path):
        super().__init__(f"\nInvalid output directory: {path}")


class ConfigPathInvalid(Exception):

    def __init__(self, path):
        super().__init__(f"\nInvalid configuration path: {path}")