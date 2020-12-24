# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyhapi\hasset.py
# Compiled at: 2020-02-03 22:05:45
# Size of source mod 2**32: 2009 bytes
__doc__ = 'Interface for interacting with houdini digital assets (hda)\nAuthor  : Maajor\nEmail   : info@ma-yidong.com\n\nHAsset:\n    Representing an HDA asset\n\nExample usage:\n\nimport pyhapi as ph\n\n#create a houdini engine session\nsession = ph.HSessionManager.get_or_create_default_session()\n\nhda_asset = ph.HAsset(session, "hda/FourShapes.hda")\nasset_node = hda_asset.instantiate(node_name="Processor").cook()\n'
from . import hapi as HAPI
from .hnode import HNode

class HAsset:
    """HAsset"""

    def __init__(self, session, hdapath):
        """Initialize

        Args:
            session (int64): The session of Houdini you are interacting with.
            hdapath (str): Path of loading hda
        """
        self.instantiated = False
        self.hda_path = hdapath
        self.session = session
        asset_lib_id = HAPI.load_asset_library_from_file(session.hapi_session, self.hda_path)
        self.asset_names = HAPI.get_available_assets(session.hapi_session, asset_lib_id)

    def instantiate(self, node_name='Node', operator_id=0):
        """Instantiate an operator in this node

        Args:
            node_name (str, optional): Assign a name for this node. Defaults to "Node".
            operator_id (int, optional): Operator id you want to instantiate in this asset.                 Defaults to 0.

        Returns:
            HNode: Node instantiated
        """
        node = HNode(self.session, self.asset_names[operator_id], node_name)
        return node

    def get_assets_names(self):
        """Get all operator names in this asset
        """
        return self.asset_names