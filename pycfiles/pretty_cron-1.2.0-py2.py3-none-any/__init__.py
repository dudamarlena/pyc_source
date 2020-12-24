# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pretty_bad_protocol/__init__.py
# Compiled at: 2018-07-25 15:08:25
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
gnupg.__version__ = __version__
gnupg.__authors__ = __authors__
gnupg.__licence__ = __license__
gnupg.__copyleft__ = __copyleft__
gnupg._logger = _logger
gnupg._meta = _meta
gnupg._parsers = _parsers
gnupg._util = _util
__all__ = [
 'GPG', '_util', '_parsers', '_meta', '_logger']
del absolute_import
del copyleft
del get_versions
del _version