# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/picage-project/picage/__init__.py
# Compiled at: 2019-10-01 10:56:34
# Size of source mod 2**32: 487 bytes
from ._version import __version__
__short_description__ = 'Object style interface for package/module.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .helpers import SP_DIR, get_sp_dir, is_valid_package_module_name
    from .model import Module, Package
except Exception as e:
    pass