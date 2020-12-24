# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Warnings.py
# Compiled at: 2016-07-07 03:21:31
"""SCons.Warnings

This file implements the warnings framework for SCons.

"""
__revision__ = 'src/engine/SCons/Warnings.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import sys, SCons.Errors

class Warning(SCons.Errors.UserError):
    pass


class WarningOnByDefault(Warning):
    pass


class TargetNotBuiltWarning(Warning):
    pass


class CacheVersionWarning(WarningOnByDefault):
    pass


class CacheWriteErrorWarning(Warning):
    pass


class CorruptSConsignWarning(WarningOnByDefault):
    pass


class DependencyWarning(Warning):
    pass


class DevelopmentVersionWarning(WarningOnByDefault):
    pass


class DuplicateEnvironmentWarning(WarningOnByDefault):
    pass


class FutureReservedVariableWarning(WarningOnByDefault):
    pass


class LinkWarning(WarningOnByDefault):
    pass


class MisleadingKeywordsWarning(WarningOnByDefault):
    pass


class MissingSConscriptWarning(WarningOnByDefault):
    pass


class NoMD5ModuleWarning(WarningOnByDefault):
    pass


class NoMetaclassSupportWarning(WarningOnByDefault):
    pass


class NoObjectCountWarning(WarningOnByDefault):
    pass


class NoParallelSupportWarning(WarningOnByDefault):
    pass


class ReservedVariableWarning(WarningOnByDefault):
    pass


class StackSizeWarning(WarningOnByDefault):
    pass


class VisualCMissingWarning(WarningOnByDefault):
    pass


class VisualVersionMismatch(WarningOnByDefault):
    pass


class VisualStudioMissingWarning(Warning):
    pass


class FortranCxxMixWarning(LinkWarning):
    pass


class FutureDeprecatedWarning(Warning):
    pass


class DeprecatedWarning(Warning):
    pass


class MandatoryDeprecatedWarning(DeprecatedWarning):
    pass


class PythonVersionWarning(DeprecatedWarning):
    pass


class DeprecatedSourceCodeWarning(FutureDeprecatedWarning):
    pass


class DeprecatedBuildDirWarning(DeprecatedWarning):
    pass


class TaskmasterNeedsExecuteWarning(DeprecatedWarning):
    pass


class DeprecatedCopyWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedOptionsWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedSourceSignaturesWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedTargetSignaturesWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedDebugOptionsWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedSigModuleWarning(MandatoryDeprecatedWarning):
    pass


class DeprecatedBuilderKeywordsWarning(MandatoryDeprecatedWarning):
    pass


_enabled = []
_warningAsException = 0
_warningOut = None

def suppressWarningClass(clazz):
    """Suppresses all warnings that are of type clazz or
    derived from clazz."""
    global _enabled
    _enabled.insert(0, (clazz, 0))


def enableWarningClass(clazz):
    """Enables all warnings that are of type clazz or
    derived from clazz."""
    _enabled.insert(0, (clazz, 1))


def warningAsException(flag=1):
    """Turn warnings into exceptions.  Returns the old value of the flag."""
    global _warningAsException
    old = _warningAsException
    _warningAsException = flag
    return old


def warn(clazz, *args):
    global _warningOut
    warning = clazz(args)
    for clazz, flag in _enabled:
        if isinstance(warning, clazz):
            if flag:
                if _warningAsException:
                    raise warning
                if _warningOut:
                    _warningOut(warning)
            break


def process_warn_strings(arguments):
    """Process string specifications of enabling/disabling warnings,
    as passed to the --warn option or the SetOption('warn') function.
    

    An argument to this option should be of the form <warning-class>
    or no-<warning-class>.  The warning class is munged in order
    to get an actual class name from the classes above, which we
    need to pass to the {enable,disable}WarningClass() functions.
    The supplied <warning-class> is split on hyphens, each element
    is capitalized, then smushed back together.  Then the string
    "Warning" is appended to get the class name.

    For example, 'deprecated' will enable the DeprecatedWarning
    class.  'no-dependency' will disable the DependencyWarning class.

    As a special case, --warn=all and --warn=no-all will enable or
    disable (respectively) the base Warning class of all warnings.

    """

    def _capitalize(s):
        if s[:5] == 'scons':
            return 'SCons' + s[5:]
        else:
            return s.capitalize()

    for arg in arguments:
        elems = arg.lower().split('-')
        enable = 1
        if elems[0] == 'no':
            enable = 0
            del elems[0]
        if len(elems) == 1 and elems[0] == 'all':
            class_name = 'Warning'
        else:
            class_name = ('').join(map(_capitalize, elems)) + 'Warning'
        try:
            clazz = globals()[class_name]
        except KeyError:
            sys.stderr.write("No warning type: '%s'\n" % arg)
        else:
            if enable:
                enableWarningClass(clazz)
            elif issubclass(clazz, MandatoryDeprecatedWarning):
                fmt = "Can not disable mandataory warning: '%s'\n"
                sys.stderr.write(fmt % arg)
            else:
                suppressWarningClass(clazz)