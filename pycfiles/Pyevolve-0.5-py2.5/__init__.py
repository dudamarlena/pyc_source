# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyevolve\__init__.py
# Compiled at: 2009-01-21 20:08:08
"""
:mod:`pyevolve` -- the main pyevolve namespace
================================================================

This is the main module of the pyevolve, every other module
is above this namespace, for example, to import :mod:`Mutators`:

   >>> from pyevolve import Mutators

"""
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