# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/tagger/widgets/taggereditor.py
# Compiled at: 2020-05-04 02:49:13
# Size of source mod 2**32: 2430 bytes
"""
Module that contains core implementation for tagger editors
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtCore import *
from tpDcc.libs.python import decorators
from tpDcc.libs.qt.core import base
import artellapipe

class TaggerEditor(base.BaseWidget, object):
    dataUpdated = Signal()
    EDITOR_TYPE = None

    def __init__(self, project, parent=None):
        self._project = project
        super(TaggerEditor, self).__init__(parent=parent)

    @property
    def project(self):
        """
        Returns project associated to this editor
        :return: ArtellaProject
        """
        return self._project

    @decorators.abstractmethod
    def initialize(self):
        """
        Initializes tagger editor
        """
        raise NotImplementedError('initialize() function not implemented in {}'.format(self.__class__.__name__))

    @decorators.abstractmethod
    def update_tag_buttons_state(self, sel=None):
        """
        Updates the state of the tag buttons
        :param sel: list(str)
        """
        raise NotImplementedError('update_tag_buttons_state() function not implemented in {}'.format(self.__class__.__name__))

    @decorators.abstractmethod
    def fill_tag_node(self, tag_data_node, *args, **kwargs):
        """
        Fills given tag node with the data managed by this editor
        :param tag_data_node: str
        """
        raise NotImplementedError('fill_tag_node() function not implemented in {}'.format(self.__class__.__name__))

    @decorators.abstractmethod
    def reset(self):
        """
        Function that resets all editor information
        """
        raise NotImplementedError('reset() function not implemented in {}'.format(self.__class__.__name__))

    def update_data(self, data=None, *args, **kwargs):
        """
        Update the data in the tag data node that is managed by this editor
        :param data: variant
        """
        sel = kwargs.pop('sel', None)
        tag_data_node = artellapipe.TagsMgr().get_tag_data_node_from_current_selection(sel)
        if tag_data_node is None:
            return
        (self.fill_tag_node)(tag_data_node, *args, data=data, **kwargs)
        self.dataUpdated.emit()