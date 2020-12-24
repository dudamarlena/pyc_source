# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gnupg/__init__.py
# Compiled at: 2014-06-04 15:52:05
from __future__ import absolute_import
from . import gnupg
from . import copyleft
from . import _ansistrm
from . import _logger
from . import _meta
from . import _parsers
from . import _util
from .gnupg import GPG
from ._version import get_versions
__version__ = get_versions()['version']
__authors__ = copyleft.authors
__license__ = copyleft.full_text
__copyleft__ = copyleft.copyright
__all__ = [
 'GPG', '_util', '_parsers', '_meta', '_logger']
del gnupg
del absolute_import
del copyleft
del get_versions
del _version