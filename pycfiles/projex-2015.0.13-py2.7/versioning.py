# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/versioning.py
# Compiled at: 2016-07-03 23:28:12
""" Defines common and useful methods for version comparison. """
import re
from .sorting import natural as vercmp
from . import errors

def validate(version, comparison):
    """
    Returns whether or not the version for this plugin satisfies the
    inputted expression.  The expression will follow the dependency
    declaration rules associated with setuptools in Python.  More
    information can be found at
    
    [https://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies]
    
    :param      version     | <str>
                expression  | <str>
    
    :return     <bool>
    """
    if not comparison:
        return True
    opts = comparison.split(',')
    expr = re.compile('(==|!=|<=|>=|<|>)(.*)')
    for opt in opts:
        try:
            test, value = expr.match(opt.strip()).groups()
        except StandardError:
            raise errors.InvalidVersionDefinition(opt)

        value = value.strip()
        if test == '==':
            if value == version:
                return True
        elif test == '!=':
            if value == version:
                return False
        elif test == '<':
            if vercmp(version, value) != -1:
                return False
        elif test == '<=':
            if vercmp(version, value) not in (-1, 0):
                return False
        elif test == '>':
            if vercmp(value, version) != -1:
                return False
        elif test == '>=':
            if vercmp(value, version) not in (-1, 0):
                return False

    return True