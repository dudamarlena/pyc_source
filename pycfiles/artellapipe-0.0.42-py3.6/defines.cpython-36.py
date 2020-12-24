# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/core/defines.py
# Compiled at: 2020-04-17 19:05:38
# Size of source mod 2**32: 2320 bytes
"""
Module that contains all constant definitions used by artellapipe
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'

class ArtellaFileStatus(object):
    WORKING = 'working'
    PUBLISHED = 'published'
    ALL = 'All'

    @classmethod
    def is_valid(cls, status):
        """
        Returns whether given status is valid or not
        :param status: str
        :return: bool
        """
        return status == cls.WORKING or status == cls.PUBLISHED or status == cls.ALL

    @classmethod
    def supported_statuses(cls):
        """
        Returns list of supported Artella Asset File Statuses
        :return: list(str)
        """
        return (
         cls.WORKING, cls.PUBLISHED, cls.ALL)


ARTELLA_PROJECT_CHANGELOG_FILE_NAME = 'changelog.yml'
ARTELLA_CONFIG_OUTLINER_CATEGORIES_ATTRIBUTE_NAME = 'OUTLINER_CATEGORIES'
ARTELLA_CONFIG_SHOT_REGEX_ATTRIBUTE_NAME = 'SHOT_REGEX'
ARTELLA_SHOT_EXTENSION_ATTRIBUTE_NAME = 'SHOT_EXTENSION'
ARTELLA_SHOT_FILE_TYPES_ATTRIBUTE_NAME = 'SHOT_FILE_TYPES'
ARTELLA_CONFIG_ASSET_PUBLISH_STATUS = 'ASSET_PUBLISH_STATUS'
ARTELLA_CONFIG_ENVIRONMENT_VARIABLE = 'PROJECT_ENV_VARIABLE'
ARTELLA_CONFIG_FOLDERS_TO_REGISTER_ATTRIBUTE_NAME = 'PATHS_TO_REGISTER'
ARTELLA_SHOT_OVERRIDES_ATTRIBUTE_PREFX = 'shot_overrides'
ARTELLA_SHOT_OVERRIDES_ATTRIBUTE_SEPARATOR = '__'