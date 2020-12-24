# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/app/pdbcheck.py
# Compiled at: 2008-06-27 12:03:50
import sys, pdb, logging
logger = logging.getLogger('cluemapper')

class PDBCheckFilter(object):
    """Middleware for handling debugging.

      >>> import traceback, sys
      >>> from clue.tools.testing import Mock
      >>> def debug(tb):
      ...     print 'Error correctly raised'
      >>> f = PDBCheckFilter(lambda x,y: None, None)
      >>> f.debug = debug
      >>> f.logger = Mock(error=lambda x: None)
      >>> f(None, None)

      >>> def raiseerr(x, y): raise ValueError('test error')
      >>> f.app = raiseerr
      >>> f(None, None)
      Error correctly raised

    """
    debug = pdb.post_mortem
    logger = logger

    def __init__(self, app, global_conf):
        self.app = app
        self.global_conf = global_conf

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            self.logger.error('Caught error, starting post-mortem debugger')
            tb = sys.exc_info()[2]
            self.debug(tb)


make_filter = PDBCheckFilter