# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/outliner/widgets/baseoutliner.py
# Compiled at: 2020-05-04 02:54:08
# Size of source mod 2**32: 10100 bytes
"""
Module that contains different outliners for Artella Outliner
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging.config
from functools import partial
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
import tpDcc as tp, artellapipe
from artellapipe.tools.outliner.core import outlinertree
from artellapipe.tools.outliner.widgets import items
LOGGER = logging.getLogger()

class BaseOutliner(outlinertree.OutlinerTree, object):
    __doc__ = '\n    Base class to create outliners\n    '
    OUTLINER_ITEM = items.OutlinerAssetItem

    def __init__(self, project, parent=None):
        super(BaseOutliner, self).__init__(project=project, parent=parent)

    def _init(self):
        assets = artellapipe.AssetsMgr().get_scene_assets(allowed_types=(self.CATEGORIES),
          allowed_tags=(self.CATEGORIES)) or list()
        for asset in assets:
            asset_widget = self.OUTLINER_ITEM(asset)
            asset_widget.contextRequested.connect(self._on_show_context_menu)
            asset_widget.clicked.connect(self._on_item_clicked)
            asset_widget.viewToggled.connect(self._on_toggle_view)
            self.append_widget(asset_widget)
            self._widget_tree[asset_widget] = list()
            overrides = asset.get_overrides()
            if overrides:
                for override in overrides:
                    self._add_override(override=override, parent=asset_widget)

    def _add_override(self, override, parent):
        """
        Internal function that appends given override widget into the parent asset item widget
        :param override: OverrideAssetItem
        :param parent: OutlinerAssetItem
        """
        override_widget = items.OutlinerOverrideItem(override=override, parent=parent)
        override_widget.removed.connect(partial(self._on_override_removed, override, parent))
        parent.add_child(override_widget, name=(override.OVERRIDE_NAME))

    def _create_context_menu(self, menu, item):
        """
        Internal function that creates context menu for the given item
        :param menu: QMenu
        :param item: OutlinerItem
        """
        pass

    def _on_item_clicked--- This code section failed: ---

 L.  96         0  LOAD_FAST                'widget'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.  97         8  LOAD_GLOBAL              LOGGER
               10  LOAD_ATTR                warning
               12  LOAD_STR                 'Selected Asset is not valid!'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  POP_TOP          

 L.  98        18  LOAD_CONST               None
               20  RETURN_END_IF    
             22_0  COME_FROM             6  '6'

 L. 100        22  LOAD_FAST                'widget'
               24  LOAD_ATTR                asset_node
               26  LOAD_ATTR                name
               28  STORE_FAST               'asset_name'

 L. 101        30  LOAD_FAST                'widget'
               32  LOAD_ATTR                is_selected
               34  STORE_FAST               'item_state'

 L. 102        36  LOAD_GLOBAL              tp
               38  LOAD_ATTR                Dcc
               40  LOAD_ATTR                object_exists
               42  LOAD_FAST                'asset_name'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  POP_JUMP_IF_FALSE   204  'to 204'

 L. 103        48  LOAD_FAST                'event'
               50  LOAD_ATTR                modifiers
               52  CALL_FUNCTION_0       0  '0 positional arguments'
               54  LOAD_GLOBAL              Qt
               56  LOAD_ATTR                ControlModifier
               58  COMPARE_OP               ==
               60  STORE_FAST               'is_modified'

 L. 104        62  LOAD_FAST                'is_modified'
               64  POP_JUMP_IF_TRUE     76  'to 76'

 L. 105        66  LOAD_GLOBAL              tp
               68  LOAD_ATTR                Dcc
               70  LOAD_ATTR                clear_selection
               72  CALL_FUNCTION_0       0  '0 positional arguments'
               74  POP_TOP          
             76_0  COME_FROM            64  '64'

 L. 107        76  SETUP_LOOP          176  'to 176'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _widget_tree
               82  LOAD_ATTR                items
               84  CALL_FUNCTION_0       0  '0 positional arguments'
               86  GET_ITER         
               88  FOR_ITER            174  'to 174'
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'asset_widget'
               94  STORE_FAST               'file_items'

 L. 108        96  LOAD_FAST                'asset_widget'
               98  LOAD_FAST                'widget'
              100  COMPARE_OP               !=
              102  POP_JUMP_IF_FALSE   134  'to 134'

 L. 109       104  LOAD_FAST                'is_modified'
              106  POP_JUMP_IF_FALSE   124  'to 124'

 L. 110       108  LOAD_FAST                'asset_widget'
              110  LOAD_ATTR                is_selected
              112  POP_JUMP_IF_TRUE    132  'to 132'

 L. 111       114  LOAD_FAST                'asset_widget'
              116  LOAD_ATTR                deselect
              118  CALL_FUNCTION_0       0  '0 positional arguments'
              120  POP_TOP          
              122  JUMP_ABSOLUTE       172  'to 172'
              124  ELSE                     '132'

 L. 113       124  LOAD_FAST                'asset_widget'
              126  LOAD_ATTR                deselect
              128  CALL_FUNCTION_0       0  '0 positional arguments'
              130  POP_TOP          
            132_0  COME_FROM           112  '112'
              132  JUMP_BACK            88  'to 88'
              134  ELSE                     '172'

 L. 115       134  LOAD_FAST                'is_modified'
              136  POP_JUMP_IF_FALSE    88  'to 88'
              138  LOAD_FAST                'widget'
              140  LOAD_ATTR                is_selected
              142  POP_JUMP_IF_FALSE    88  'to 88'

 L. 116       144  LOAD_FAST                'asset_widget'
              146  LOAD_ATTR                select
              148  CALL_FUNCTION_0       0  '0 positional arguments'
              150  POP_TOP          

 L. 117       152  LOAD_GLOBAL              tp
              154  LOAD_ATTR                Dcc
              156  LOAD_ATTR                select_object
              158  LOAD_FAST                'asset_widget'
              160  LOAD_ATTR                asset_node
              162  LOAD_ATTR                name
              164  LOAD_CONST               True
              166  LOAD_CONST               ('add',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          
              172  JUMP_BACK            88  'to 88'
              174  POP_BLOCK        
            176_0  COME_FROM_LOOP       76  '76'

 L. 125       176  LOAD_FAST                'widget'
              178  LOAD_ATTR                set_select
              180  LOAD_FAST                'item_state'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  POP_TOP          

 L. 126       186  LOAD_FAST                'is_modified'
              188  POP_JUMP_IF_TRUE    212  'to 212'

 L. 127       190  LOAD_GLOBAL              tp
              192  LOAD_ATTR                Dcc
              194  LOAD_ATTR                select_object
              196  LOAD_FAST                'asset_name'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_FORWARD        212  'to 212'
              204  ELSE                     '212'

 L. 129       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _on_refresh_outliner
              208  CALL_FUNCTION_0       0  '0 positional arguments'
              210  POP_TOP          
            212_0  COME_FROM           202  '202'
            212_1  COME_FROM           188  '188'

Parse error at or near `ELSE' instruction at offset 134

    def _on_toggle_view(self, widget):
        node_name = widget.asset_node.node
        if tp.Dcc.object_exists(node_name):
            if tp.Dcc.node_is_visible(node_name):
                tp.Dcc.hide_object(node_name)
                widget.display_buttons.hide()
            else:
                tp.Dcc.show_object(node_name)
                widget.display_buttons.show()

    def _on_remove(self, item):
        """
        Internal callback function that is called when Delete context action is triggered
        """
        valid_remove = item.asset_node.remove()
        if valid_remove:
            self.remove_widget(item)
            item.removed.emit(item)

    def _create_add_override_menu(self, menu, item):
        """
        Internal function that creates the add override menu
        :param menu: QMenu
        :return: bool
        """
        try:
            registered_overrides = shotassembler.ShotAssembler.registered_overrides()
        except Exception as exc:
            LOGGER.error(exc)
            return False

        if not registered_overrides:
            return False
        else:
            for override_name, override in registered_overrides.items():
                override_action = QAction(override.OVERRIDE_ICON, override.OVERRIDE_NAME, menu)
                if self._asset_node.has_override(override):
                    override_action.setEnabled(False)
                    override_action.setText('{} | Already added!'.format(override_action.text()))
                override_action.triggered.connect(partial(self._on_add_override, override, item))
                menu.addAction(override_action)

            return True

    def _create_remove_override_menu(self, menu, item):
        """
        Internal that creates the remove overrides menu
        :param menu: QMenu
        :return: bool
        """
        node_overrides = item.asset_node.get_overrides()
        if not node_overrides:
            return False
        else:
            for override in node_overrides:
                override_action = QAction(override.OVERRIDE_ICON, override.OVERRIDE_NAME, menu)
                override_action.triggered.connect(partial(self._on_remove_override, override, item))
                menu.addAction(override_action)

            return True

    def _create_save_override_menu(self, menu, item):
        """
        Internal function that reates the save overrides menu
        :param menu: QMenu
        :return: bool
        """
        node_overrides = item.asset_node.get_overrides()
        if not node_overrides:
            return False
        else:
            added_overrides = list()
            for override in node_overrides:
                override_action = QAction(override.OVERRIDE_ICON, override.OVERRIDE_NAME, menu)
                override_action.triggered.connect(partial(self._on_save_override, override, item))
                added_overrides.append(override_action)
                menu.addAction(override_action)

            if len(added_overrides) > 0:
                menu.addSeparator()
                save_all_overrides_action = QAction(resource.ResourceManager().icon('save'), 'All', menu)
                save_all_overrides_action.triggered.connect(self._on_save_all_overrides, item)
                menu.addAction(save_all_overrides_action)
            return True

    def _on_add_override(self, new_override, item):
        """
        Internal callback function that is called when Add Override context button is pressed
        :param new_override: ArtellaBaseOverride
        """
        valid_override = self._asset_node.add_override(new_override)
        if valid_override:
            self.overrideAdded.emit(valid_override, item)

    def _on_remove_override(self, override_to_remove, item):
        """
        Internal callback function that is called when Remove Override context button is pressed
        :param override_to_remove: ArtellaBaseOverride
        """
        removed_override = self._asset_node.remove_override(override_to_remove)
        if removed_override:
            self.overrideRemoved.emit(removed_override, item)

    def _on_save_override(self, override_to_save, item):
        """
        Internal callback function that is called when Save Override context button is pressed
        :param override_to_save: ArtellaBaseOverride
        """
        item.asset_node.save_override(override_to_save)

    def _on_save_all_overrides(self, item):
        """
        Internal callback function that is called when Save All Overrides context action is triggered
        """
        item.asset_node.save_all_overrides()

    def _on_override_added(self, override, parent):
        self._add_override(override=override, parent=parent)
        parent.expand()

    def _on_override_removed(self, override, parent):
        parent.remove_child(override.OVERRIDE_NAME)

    def _on_show_context_menu(self, item):
        menu = QMenu()
        self._create_context_menu(menu, item)
        action = menu.exec_(QCursor.pos())
        return action