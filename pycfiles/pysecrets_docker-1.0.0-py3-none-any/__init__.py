# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pysecret/__init__.py
# Compiled at: 2019-04-10 22:39:08
__doc__ = '\npysecret is a tiny library to allow developer load secret information safely.\n\n- from environment variable\n- from json file\n- from AWS Secret Manager and Key Management Service\n'
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