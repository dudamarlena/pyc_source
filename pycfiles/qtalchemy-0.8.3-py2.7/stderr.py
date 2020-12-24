# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/xplatform/stderr.py
# Compiled at: 2013-09-07 09:08:02
"""
This module contains tools to enable cross platform support.

For the most part, we have functions here which do something for windows 
and something else for everything else.
"""

def guiexcepthook(type, value, tb):
    """
    Replace sys.excepthook with this function to display errors more gracefully 
    for an application which is not associated with a console.
    
    >>> import sys
    >>> from qtalchemy import xplatform
    >>> sys.excepthook = xplatform.guiexcepthook
    """
    try:
        from . import util
        import tempfile, traceback
        f = open(tempfile.mktemp(prefix='qtalchemy-error-', suffix='.txt'), 'w')
        traceback.print_exception(type, value, tb, limit=None, file=f)
        util.xdg_open(f.name)
    except:
        import sys
        traceback.print_exception(type, value, tb, limit=None, file=sys.stderr)

    return


class StdErrEater(object):
    """
    Instead of printing to stderr a GUI app may want to log the stderr stream 
    to a text file.  This is particularly relevant in cross-platform situations 
    because py2exe logs and messages the user at app exit.  We'd like to have a 
    friendlier approach.
    
    For windows, future possibilities include directing stderr lines to the 
    windows event log.
    
    A possible usage method is:

    >>> from qtalchemy import *
    >>> import sys
    >>> def exitApplication():
    ...     if isinstance(sys.stderr, xplatform.StdErrEater):
    ...         see = sys.stderr
    ...         if see.file:
    ...             fn = see.file.name
    ...             see.file.close()
    ...             see.file = None
    ... 
    ...             msgs = open(fn,"r").read()
    ...             if msgs != "":
    ...                 xplatform.xdg_open( fn )
    ...     
    >>> if xplatform.is_windows():
    ...     # We want a log of exceptions that have been sent to standard error.
    ...     # PyQt/PySide has a bad habit of not exposing these things to the user, but we absolutely must have a way to diagnose funny failures.
    ...     sys.stderr = xplatform.StdErrEater()
    ... 
    >>> # run the main body of the application
    >>> exitApplication()
    """
    ignore_these = [
     'does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point']

    def __init__(self):
        self.file = None
        return

    def init_file(self):
        import tempfile, os, datetime
        x = tempfile.gettempdir()
        file_name = os.path.join(x, ('camp_rental_error_{date}_{pid}.log').format(date=datetime.date.today().strftime('%Y%m%d'), pid=0))
        self.file = open(file_name, 'a')
        self.file.write("The following errors were logged during this program.  Please consider sending \nthem to joel@kiwistrawberry.us for him to fix.  He might further inquire about \nwhether you can reproduce the problem, but it's likely that the details below \nare sufficient to produce a fix.\n\n")

    def write(self, s):
        for i in self.ignore_these:
            if s.find(i) >= 0:
                return

        if self.file is None:
            self.init_file()
        if self.file is not None:
            self.file.write(s)
        return