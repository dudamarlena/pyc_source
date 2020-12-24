# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\__init__.py
# Compiled at: 2009-01-21 20:08:08
__doc__ = '\n:mod:`pyevolve` -- the main pyevolve namespace\n================================================================\n\nThis is the main module of the pyevolve, every other module\nis above this namespace, for example, to import :mod:`Mutators`:\n\n   >>> from pyevolve import Mutators\n\n\n'
__version__ = '0.5'
__author__ = 'Christian S. Perone'
import Consts, sys
if sys.version_info < Consts.CDefPythonRequire:
    import logging
    raise Exception('Python 2.5+ required !')
else:
    del sys

def logEnable(filename=Consts.CDefLogFile, level=Consts.CDefLogLevel):
    """ Enable the log system for pyevolve

   :param filename: the log filename
   :param level: the debugging level

   Example:
      >>> pyevolve.logEnable()

   """
    import logging
    logging.basicConfig(level=level, format='%(asctime)s [%(module)s:%(funcName)s:%(lineno)d] %(levelname)s %(message)s', filename=filename, filemode='w')