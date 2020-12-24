# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/__init__.py
# Compiled at: 2019-04-10 22:39:08
# Size of source mod 2**32: 817 bytes
"""
pysecret is a tiny library to allow developer load secret information safely.

- from environment variable
- from json file
- from AWS Secret Manager and Key Management Service
"""
from ._version import __version__
__short_description__ = 'utility tool that load secret information safely.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .helper import home_file_path
    from .env import EnvSecret
    from .js import JsonSecret, DEFAULT_JSON_SECRET_FILE
except ImportError:
    pass
except Exception as e:
    raise e

try:
    from .aws import AWSSecret
except ImportError:
    pass
except Exception as e:
    raise e