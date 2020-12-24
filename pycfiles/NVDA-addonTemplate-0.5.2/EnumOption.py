# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Options\EnumOption.py
# Compiled at: 2016-07-07 03:21:32
__revision__ = 'src/engine/SCons/Options/EnumOption.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = 'Place-holder for the old SCons.Options module hierarchy\n\nThis is for backwards compatibility.  The new equivalent is the Variables/\nclass hierarchy.  These will have deprecation warnings added (some day),\nand will then be removed entirely (some day).\n'
import SCons.Variables, SCons.Warnings
warned = False

def EnumOption(*args, **kw):
    global warned
    if not warned:
        msg = 'The EnumOption() function is deprecated; use the EnumVariable() function instead.'
        SCons.Warnings.warn(SCons.Warnings.DeprecatedOptionsWarning, msg)
        warned = True
    return SCons.Variables.EnumVariable(*args, **kw)