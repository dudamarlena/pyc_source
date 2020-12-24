# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/error.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 8, 2013

@package: ally base
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Defines the errors for the IoC module.
"""

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