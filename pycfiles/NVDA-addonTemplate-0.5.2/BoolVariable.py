# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Variables\BoolVariable.py
# Compiled at: 2016-07-07 03:21:36
"""engine.SCons.Variables.BoolVariable

This file defines the option type for SCons implementing true/false values.

Usage example:

  opts = Variables()
  opts.Add(BoolVariable('embedded', 'build for an embedded system', 0))
  ...
  if env['embedded'] == 1:
    ...
"""
__revision__ = 'src/engine/SCons/Variables/BoolVariable.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__all__ = [
 'BoolVariable']
import SCons.Errors
__true_strings = ('y', 'yes', 'true', 't', '1', 'on', 'all')
__false_strings = ('n', 'no', 'false', 'f', '0', 'off', 'none')

def _text2bool(val):
    """
    Converts strings to True/False depending on the 'truth' expressed by
    the string. If the string can't be converted, the original value
    will be returned.

    See '__true_strings' and '__false_strings' for values considered
    'true' or 'false respectively.

    This is usable as 'converter' for SCons' Variables.
    """
    lval = val.lower()
    if lval in __true_strings:
        return True
    if lval in __false_strings:
        return False
    raise ValueError('Invalid value for boolean option: %s' % val)


def _validator(key, val, env):
    """
    Validates the given value to be either '0' or '1'.
    
    This is usable as 'validator' for SCons' Variables.
    """
    if env[key] not in (True, False):
        raise SCons.Errors.UserError('Invalid value for boolean option %s: %s' % (key, env[key]))


def BoolVariable(key, help, default):
    """
    The input parameters describe a boolean option, thus they are
    returned with the correct converter and validator appended. The
    'help' text will by appended by '(yes|no) to show the valid
    valued. The result is usable for input to opts.Add().
    """
    return (
     key, '%s (yes|no)' % help, default,
     _validator, _text2bool)