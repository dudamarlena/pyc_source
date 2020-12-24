# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/windtalker-project/windtalker/__init__.py
# Compiled at: 2020-03-04 17:39:17
# Size of source mod 2**32: 593 bytes
from ._version import __version__
__short_description__ = 'Super easy-to-use encryption and decryption tool'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .cipher import BaseCipher
except ImportError:
    pass

try:
    from .symmetric import SymmetricCipher
except ImportError:
    pass

try:
    from .asymmetric import AsymmetricCipher
except ImportError:
    pass