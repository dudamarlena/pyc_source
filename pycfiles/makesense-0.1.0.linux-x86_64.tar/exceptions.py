# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/makesense/exceptions.py
# Compiled at: 2014-10-21 08:35:55
"""
Makesense.exceptions
-----------------------

All exceptions used in the Makesense code base are defined here.
"""

class MakesenseException(Exception):
    """
    Base exception class. All Makesense-specific exceptions should subclass
    this class.
    """
    pass


class NonTemplatedInputDirException(MakesenseException):
    """
    Raised when a project's input dir is not templated.
    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """
    pass


class UnknownTemplateDirException(MakesenseException):
    """
    Raised when Makesense cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """
    pass


class MissingProjectDir(MakesenseException):
    """
    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """
    pass


class ConfigDoesNotExistException(MakesenseException):
    """
    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """
    pass


class InvalidConfiguration(MakesenseException):
    """
    Raised if the global configuration file is not valid YAML or is
    badly contructed.
    """
    pass


class UnknownRepoType(MakesenseException):
    """
    Raised if a repo's type cannot be determined.
    """
    pass