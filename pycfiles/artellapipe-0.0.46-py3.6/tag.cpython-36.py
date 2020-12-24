# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/core/tag.py
# Compiled at: 2020-05-13 18:51:06
# Size of source mod 2**32: 3469 bytes
"""
Module that contains definitions for tags in Artella
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import ast, string, tpDcc as tp, artellapipe.register

class ArtellaTagNode(object):

    def __init__(self, project, node, tag_info=None):
        super(ArtellaTagNode, self).__init__()
        self._project = project
        self._node = node
        self._tag_info_dict = tag_info
        if tag_info:
            self._tag_info_dict = ast.literal_eval(tag_info)
            short_node = tp.Dcc.node_short_name(node)
            if short_node in self._tag_info_dict.keys():
                self._tag_info_dict = self._tag_info_dict[short_node]
            else:
                short_node_strip = short_node.rstrip(string.digits)
                if short_node_strip in self._tag_info_dict.keys():
                    self._tag_info_dict = self._tag_info_dict[short_node_strip]

    @property
    def node(self):
        """
        Returns linked to the tag node
        :return: str
        """
        return self._node

    @property
    def tag_info(self):
        """
        Returns tag info data stored in this node
        :return: dict
        """
        return self._tag_info_dict

    def get_clean_node(self):
        """
        Returns current node with the short name and with ids removed
        :return: str
        """
        return tp.Dcc.node_short_name(self._node).rstrip(string.digits)

    def get_asset_node(self):
        """
        Returns asset node linked to this tag node
        :return: ArtellaAssetNode
        """
        if not self._node or not tp.Dcc.object_exists(self._node):
            return
        else:
            if self._tag_info_dict:
                return artellapipe.AssetsMgr().get_asset_node_in_scene(node_id=(self._node))
            if not tp.Dcc.attribute_exists(node=(self._node),
              attribute_name=(artellapipe.TagsMgr().TagDefinitions.NODE_ATTRIBUTE_NAME)):
                return
            connections = tp.Dcc.list_connections(node=(self._node),
              attribute_name=(artellapipe.TagsMgr().TagDefinitions.NODE_ATTRIBUTE_NAME))
            if connections:
                node = connections[0]
                return artellapipe.AssetsMgr().get_asset_node_in_scene(node_id=node)

    def get_tag_type(self):
        """
        Returns the type of the tag
        :return: str
        """
        return self._get_attribute(attribute_name=(artellapipe.TagsMgr().TagDefinitions.TAG_TYPE_ATTRIBUTE_NAME))

    def _get_attribute(self, attribute_name):
        """
        Internal function that retrieves attribute from wrapped TagData node
        :param attribute_name: str, attribute name to retrieve from TagData node
        :return: variant
        """
        if self._tag_info_dict:
            return self._tag_info_dict.get(attribute_name)
        else:
            if not self._node or not tp.Dcc.object_exists(self._node):
                return
            if not tp.Dcc.attribute_exists(node=(self._node), attribute_name=attribute_name):
                return
            return tp.Dcc.get_attribute_value(node=(self._node), attribute_name=attribute_name)


artellapipe.register.register_class('TagNode', ArtellaTagNode)