# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Errors.py
# Compiled at: 2016-07-07 03:21:32
"""SCons.Errors

This file contains the exception classes used to handle internal
and user errors in SCons.

"""
__revision__ = 'src/engine/SCons/Errors.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Util, exceptions

class BuildError(Exception):
    """ Errors occuring while building.

    BuildError have the following attributes:

        Information about the cause of the build error:
        -----------------------------------------------

        errstr : a description of the error message

        status : the return code of the action that caused the build
                 error. Must be set to a non-zero value even if the
                 build error is not due to an action returning a
                 non-zero returned code.

        exitstatus : SCons exit status due to this build error.
                     Must be nonzero unless due to an explicit Exit()
                     call.  Not always the same as status, since
                     actions return a status code that should be
                     respected, but SCons typically exits with 2
                     irrespective of the return value of the failed
                     action.

        filename : The name of the file or directory that caused the
                   build error. Set to None if no files are associated with
                   this error. This might be different from the target
                   being built. For example, failure to create the
                   directory in which the target file will appear. It
                   can be None if the error is not due to a particular
                   filename.

        exc_info : Info about exception that caused the build
                   error. Set to (None, None, None) if this build
                   error is not due to an exception.

        Information about the cause of the location of the error:
        ---------------------------------------------------------

        node : the error occured while building this target node(s)
        
        executor : the executor that caused the build to fail (might
                   be None if the build failures is not due to the
                   executor failing)
        
        action : the action that caused the build to fail (might be
                 None if the build failures is not due to the an
                 action failure)

        command : the command line for the action that caused the
                  build to fail (might be None if the build failures
                  is not due to the an action failure)
        """

    def __init__(self, node=None, errstr='Unknown error', status=2, exitstatus=2, filename=None, executor=None, action=None, command=None, exc_info=(None, None, None)):
        self.errstr = errstr
        self.status = status
        self.exitstatus = exitstatus
        self.filename = filename
        self.exc_info = exc_info
        self.node = node
        self.executor = executor
        self.action = action
        self.command = command
        Exception.__init__(self, node, errstr, status, exitstatus, filename, executor, action, command, exc_info)

    def __str__(self):
        if self.filename:
            return self.filename + ': ' + self.errstr
        else:
            return self.errstr


class InternalError(Exception):
    pass


class UserError(Exception):
    pass


class StopError(Exception):
    pass


class EnvironmentError(Exception):
    pass


class MSVCError(IOError):
    pass


class ExplicitExit(Exception):

    def __init__(self, node=None, status=None, *args):
        self.node = node
        self.status = status
        self.exitstatus = status
        Exception.__init__(self, *args)


def convert_to_BuildError(status, exc_info=None):
    """
    Convert any return code a BuildError Exception.

    `status' can either be a return code or an Exception.
    The buildError.status we set here will normally be
    used as the exit status of the "scons" process.
    """
    if not exc_info and isinstance(status, Exception):
        exc_info = (
         status.__class__, status, None)
    if isinstance(status, BuildError):
        buildError = status
        buildError.exitstatus = 2
    elif isinstance(status, ExplicitExit):
        status = status.status
        errstr = 'Explicit exit, status %s' % status
        buildError = BuildError(errstr=errstr, status=status, exitstatus=status, exc_info=exc_info)
    elif isinstance(status, (StopError, UserError)):
        buildError = BuildError(errstr=str(status), status=2, exitstatus=2, exc_info=exc_info)
    elif isinstance(status, exceptions.EnvironmentError):
        try:
            filename = status.filename
        except AttributeError:
            filename = None

        buildError = BuildError(errstr=status.strerror, status=status.errno, exitstatus=2, filename=filename, exc_info=exc_info)
    elif isinstance(status, Exception):
        buildError = BuildError(errstr='%s : %s' % (status.__class__.__name__, status), status=2, exitstatus=2, exc_info=exc_info)
    elif SCons.Util.is_String(status):
        buildError = BuildError(errstr=status, status=2, exitstatus=2)
    else:
        buildError = BuildError(errstr='Error %s' % status, status=status, exitstatus=2)
    return buildError