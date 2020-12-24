# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Variables\PathVariable.py
# Compiled at: 2016-07-07 03:21:36
"""SCons.Variables.PathVariable

This file defines an option type for SCons implementing path settings.

To be used whenever a user-specified path override should be allowed.

Arguments to PathVariable are:
  option-name  = name of this option on the command line (e.g. "prefix")
  option-help  = help string for option
  option-dflt  = default value for this option
  validator    = [optional] validator for option value.  Predefined
                 validators are:

                     PathAccept -- accepts any path setting; no validation
                     PathIsDir  -- path must be an existing directory
                     PathIsDirCreate -- path must be a dir; will create
                     PathIsFile -- path must be a file
                     PathExists -- path must exist (any type) [default]

                 The validator is a function that is called and which
                 should return True or False to indicate if the path
                 is valid.  The arguments to the validator function
                 are: (key, val, env).  The key is the name of the
                 option, the val is the path specified for the option,
                 and the env is the env to which the Options have been
                 added.

Usage example:

  Examples:
      prefix=/usr/local

  opts = Variables()

  opts = Variables()
  opts.Add(PathVariable('qtdir',
                      'where the root of Qt is installed',
                      qtdir, PathIsDir))
  opts.Add(PathVariable('qt_includes',
                      'where the Qt includes are installed',
                      '$qtdir/includes', PathIsDirCreate))
  opts.Add(PathVariable('qt_libraries',
                      'where the Qt library is installed',
                      '$qtdir/lib'))

"""
__revision__ = 'src/engine/SCons/Variables/PathVariable.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__all__ = [
 'PathVariable']
import os, os.path, SCons.Errors

class _PathVariableClass(object):

    def PathAccept(self, key, val, env):
        """Accepts any path, no checking done."""
        pass

    def PathIsDir(self, key, val, env):
        """Validator to check if Path is a directory."""
        if not os.path.isdir(val):
            if os.path.isfile(val):
                m = 'Directory path for option %s is a file: %s'
            else:
                m = 'Directory path for option %s does not exist: %s'
            raise SCons.Errors.UserError(m % (key, val))

    def PathIsDirCreate(self, key, val, env):
        """Validator to check if Path is a directory,
           creating it if it does not exist."""
        if os.path.isfile(val):
            m = 'Path for option %s is a file, not a directory: %s'
            raise SCons.Errors.UserError(m % (key, val))
        if not os.path.isdir(val):
            os.makedirs(val)

    def PathIsFile(self, key, val, env):
        """Validator to check if Path is a file"""
        if not os.path.isfile(val):
            if os.path.isdir(val):
                m = 'File path for option %s is a directory: %s'
            else:
                m = 'File path for option %s does not exist: %s'
            raise SCons.Errors.UserError(m % (key, val))

    def PathExists(self, key, val, env):
        """Validator to check if Path exists"""
        if not os.path.exists(val):
            m = 'Path for option %s does not exist: %s'
            raise SCons.Errors.UserError(m % (key, val))

    def __call__(self, key, help, default, validator=None):
        """
        The input parameters describe a 'path list' option, thus they
        are returned with the correct converter and validator appended. The
        result is usable for input to opts.Add() .

        The 'default' option specifies the default path to use if the
        user does not specify an override with this option.

        validator is a validator, see this file for examples
        """
        if validator is None:
            validator = self.PathExists
        if SCons.Util.is_List(key) or SCons.Util.is_Tuple(key):
            return (key, '%s ( /path/to/%s )' % (help, key[0]), default,
             validator, None)
        else:
            return (
             key, '%s ( /path/to/%s )' % (help, key), default,
             validator, None)
            return


PathVariable = _PathVariableClass()