# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/asset.py
# Compiled at: 2020-05-04 03:27:08
# Size of source mod 2**32: 8423 bytes
"""
Module that contains definitions for asset in Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging
from tpDcc.libs.python import python
import artellapipe.register
from artellapipe.core import defines, asset as artella_asset
LOGGER = logging.getLogger()

class SolsticeAsset(artella_asset.ArtellaAsset, object):

    def __init__(self, project, asset_data, node=None):
        super(SolsticeAsset, self).__init__(project=project, asset_data=asset_data, node=node)

    def get_tags(self):
        """
        Returns tags of the asset
        Overrides ArtellaAsset get_tags function
        :return: list(str)
        """
        asset_metadata = self.data or dict()
        kitsu_asset = asset_metadata.get('asset', None)
        if not kitsu_asset:
            tags = list()
        else:
            kitsu_data = kitsu_asset.data or dict()
            tags = kitsu_data.get('tags', list())
        tags = python.force_list(tags)
        return tags

    def reference_rig_file(self, file_type, sync=False):
        """
        References rig file of the current asset
        """
        return self.reference_file(file_type=file_type,
          namespace=(self.get_id()),
          status=(defines.ArtellaFileStatus.PUBLISHED),
          sync=sync)

    def reference_alembic_file(self, file_type, model_type, sync=False):
        """
        References Alembic file of the current asset
        :param namespace: str
        :param fix_path: bool
        """
        model_file_type = self.get_file_type(model_type)
        latest_published_local_versions = model_file_type.get_latest_local_published_version()
        if not latest_published_local_versions:
            LOGGER.warning('Asset {} has not model publsihed files synced!'.format(self.get_name()))
            return
        file_type_extensions = artellapipe.AssetsMgr().get_file_type_extensions(file_type)
        if not file_type_extensions:
            LOGGER.warning('Impossible to retrieve registered extensions from file type: "{}"'.format(file_type))
            return
        abc_extension = file_type_extensions[0]
        alembic_file_type = self.get_file_type(model_type, abc_extension)
        if not alembic_file_type:
            LOGGER.warning('Asset {} has not Alembic File published!')
            return
        self.reference_file(file_type=model_type,
          namespace=(self.get_id()),
          extension=abc_extension,
          status=(defines.ArtellaFileStatus.PUBLISHED),
          sync=sync)


artellapipe.register.register_class('Asset', SolsticeAsset)