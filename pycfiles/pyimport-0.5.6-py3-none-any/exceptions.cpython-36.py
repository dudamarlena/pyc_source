# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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