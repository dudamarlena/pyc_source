# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bu_cascade/assets/asset.py
# Compiled at: 2019-10-30 15:19:36
# Size of source mod 2**32: 2747 bytes
from bu_cascade.asset_tools import convert_asset

class Asset(object):

    def __init__(self, ws_connector, identifier, asset_type, asset_specific_key):
        self.ws = ws_connector
        self.identifier = identifier
        self.asset_type = asset_type
        self.asset_specific_key = asset_specific_key
        self.asset = None
        self.metadata = None
        self.structured_data = None

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_asset(self):
        return (
         self.asset, self.metadata, self.structured_data)

    def set_asset(self, asset):
        self.asset = asset
        self.metadata = self.get_metadata()
        self.structured_data = self.get_structured_data()

    def read_asset(self):
        asset_structure = self.ws.read(self.identifier, self.asset_type)
        asset_structure = convert_asset(asset_structure)
        if asset_structure['success'] == 'true':
            asset_structure = asset_structure['asset']
        self.set_asset(asset_structure)
        self.metadata = self.get_metadata()
        self.structured_data = self.get_structured_data()
        return self.get_asset()

    def create_asset(self, asset):
        new_id = self.ws.create(asset)['createdAssetId']
        self.set_identifier(new_id)
        return self.read_asset()

    def edit_asset(self, asset):
        return self.ws.edit(asset)

    def delete_asset(self):
        return self.ws.delete(self.identifier, self.asset_type)

    def publish_asset(self):
        return self.ws.publish(self.identifier, self.asset_type)

    def unpublish_asset(self):
        return self.ws.unpublish(self.identifier, self.asset_type)

    def move_asset(self, folder_identifier):
        return self.ws.move(self.identifier, folder_identifier, self.asset_type)

    def copy_asset(self, new_folder_identifier, new_name):
        return self.ws.copy(self.identifier, self.asset_type, new_folder_identifier, new_name)

    def rename_asset(self, new_name):
        return self.ws.rename(self.identifier, new_name, self.asset_type)

    def is_in_workflow_asset(self):
        return self.ws.is_in_workflow(self.identifier, self.asset_type)

    def get_metadata(self):
        try:
            return self.asset[self.asset_specific_key]['metadata']
        except:
            return

    def get_structured_data(self):
        try:
            return self.asset[self.asset_specific_key]['structuredData']
        except:
            return