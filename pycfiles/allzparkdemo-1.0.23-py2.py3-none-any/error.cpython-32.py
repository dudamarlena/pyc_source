# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/error.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 8, 2013\n\n@package: ally base\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nDefines the errors for the IoC module.\n'

class SetupError(Exception):
    """
    Exception thrown when there is a setup problem.
    """
    pass


class ConfigError(Exception):
    """
    Exception thrown when there is a configuration problem.
    """
    pass


class AOPError(Exception):
    """
    Exception thrown when there is a AOP problem.
    """
    pass


class WireError(Exception):
    """
    Exception thrown when there is a wiring problem.
    """
    pass


class AventError(Exception):
    """
    Exception thrown when there is an event problem.
    """
    pass