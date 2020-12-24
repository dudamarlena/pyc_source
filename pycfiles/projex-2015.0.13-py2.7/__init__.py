# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/__init__.py
# Compiled at: 2016-07-03 23:28:12
"""
This is the core Python package for all of the projex software
projects.  At the bare minimum, this package will be required, and 
depending on which software you are interested in, other packages 
will be required and updated.
"""
__authors__ = [
 'Eric Hulser']
__author__ = (',').join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2011-2016'
__license__ = 'MIT'
__maintainer__ = 'Eric Hulser'
__email__ = 'eric.hulser@gmail.com'
try:
    from ._version import __major__, __minor__, __revision__, __hash__
except ImportError:
    __major__ = 0
    __minor__ = 0
    __revision__ = 0
    __hash__ = ''

__version_info__ = (__major__, __minor__, __revision__)
__version__ = ('{0}.{1}.{2}').format(*__version_info__)
from projex.init import *
import logging
if not hasattr(logging, 'SUCCESS'):
    logging.SUCCESS = 25