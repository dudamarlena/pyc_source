# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Streamline/pyimport/pyimport/exceptions.py
# Compiled at: 2020-03-10 20:03:38
# Size of source mod 2**32: 643 bytes


class PathDoesNotExist(Exception):

    def __init__(self, name):
        msg = f"The path '{name}' does not exist"
        super().__init__(msg)


class ModuleDoesNotExist(Exception):

    def __init__(self, name):
        msg = f"The module '{name}' does not exist"
        super().__init__(msg)


class ObjectDoesNotExist(Exception):

    def __init__(self, name):
        msg = f"The object '{name}' does not exist"
        super().__init__(msg)


class InitMissing(Exception):

    def __init__(self, folder):
        msg = f"The folder '{folder}' has no file called __init__.py"
        super().__init__(msg)