# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/nosexunit/excepts.py
# Compiled at: 2009-09-22 16:55:25


class NoseXUnitError(StandardError):
    """Super class of error for NoseXunit"""
    pass


class PluginError(NoseXUnitError):
    """Class of exception for plug in"""
    pass


class CoreError(NoseXUnitError):
    """Class of exception for XUnit"""
    pass


class AuditError(NoseXUnitError):
    """Class of exception for PyLint"""
    pass


class CoverError(NoseXUnitError):
    """Class of exception for Coverage"""
    pass


class ToolError(NoseXUnitError):
    """Class of exception for tools"""
    pass