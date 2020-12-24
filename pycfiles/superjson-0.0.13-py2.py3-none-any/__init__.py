# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: superjson/__init__.py
# Compiled at: 2019-04-10 22:47:40
from ._version import __version__
__short_description__ = 'Extendable json encode/decode library.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from ._superjson import SuperJson, get_class_name, superjson as json
except ImportError as e:
    pass
except Exception as e:
    raise e