# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/zapi_script_options.py
# Compiled at: 2009-03-28 00:57:22
__revision__ = '$Revision: 1.61 $'
from options import BaseOptions
import logging, debug
from twisted.python import log as tlog
log = logging.getLogger('modipy')

class ZAPIScriptOptions(BaseOptions):

    def __init__(self, *args, **kwargs):
        """
        Initialise a base level options parser.
        """
        optparse.OptionParser.__init__(self, **kwargs)
        help_debug = 'Set the output debug level to: debug, info, warn, error, or critical.'

    def addOptions(self):
        """
        Override this method in subclasses to add more options.
        This enables multiple inheritence from the common base class.
        """
        pass

    def parseOptions(self, argv=sys.argv[1:]):
        """
        Emulate the twisted options parser API.
        """
        (options, args) = self.parse_args(argv)
        self.options = options
        self.args = args
        self.postOptions()

    def postOptions(self):
        """
        Perform post options parsing operations.
        """
        log.setLevel(logging._levelNames.get(self.options.debug.upper(), logging.INFO))