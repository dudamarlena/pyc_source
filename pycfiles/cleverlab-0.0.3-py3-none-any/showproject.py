# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/plugins/showproject.py
# Compiled at: 2006-08-02 05:57:50
from harold.plugins.lib import HaroldCommandType

class ShowProject(HaroldCommandType):
    """ Shows a Clever Harold project configuration and more.

    This isn't finished.  Ideas:

    - ini file summary, server, database, connection, but not all middleware
    - code metrics, number of files, lines, classes, functions
    
    """
    __module__ = __name__
    min_args = 1
    max_args = 1
    summary = 'Show Clever Harold project setup'
    parser = HaroldCommandType.standard_parser(verbose=True)

    def command(self):
        if self.verbose:
            print 'Verbose show'
        print 'Nothing yet to show'