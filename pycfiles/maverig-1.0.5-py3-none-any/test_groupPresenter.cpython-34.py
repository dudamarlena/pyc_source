# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_groupPresenter.py
# Compiled at: 2014-11-05 09:49:41
# Size of source mod 2**32: 17098 bytes
import sys, locale, gettext
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.data import config
from maverig.presenter.group_presenter.iconGroupPresenter import IconGroupPresenter
from maverig.presenter.group_presenter.nodeGroupPresenter import NodeGroupPresenter
from maverig.presenter.presenterManager import PresenterManager
from maverig.models.model import Model
from maverig.data.components.abstractComponent import ElemPort
from maverig.views.attributePanelView import AttributePanelView
from maverig.views.menuBarView import MenuBarView
from maverig.views.propertyPanelView import PropertyPanelView
from maverig.views.scenarioPanelView import ScenarioPanelView
from maverig.views.statusBarView import StatusBarView
from maverig.views.toolbarView import ToolbarView
from maverig.views.groups.iconGroup import IconGroup
from maverig.views.groups.nodeGroup import NodeGroup
from maverig.views.positioning.vPoint import VPoint, Change
from maverig.views.positioning.section import section_manager
from maverig.data import dataHandler
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestGroupPresenter(TestCase):

    def __init_test_environment(self):
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        self.graphics_view = QtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.graphics_view.setScene(self.scene)
        self.model = Model()
        self.presenter_manager = PresenterManager(self.model)
        attribute_panel_view = AttributePanelView()
        menu_bar_view = MenuBarView()
        property_panel_view = PropertyPanelView()
        scenario_view = ScenarioPanelView()
        status_bar_view = StatusBarView()
        toolbar_view = ToolbarView()
        self.presenter_manager.attribute_panel_presenter.view = attribute_panel_view
        self.presenter_manager.menu_bar_presenter.view = menu_bar_view
        self.presenter_manager.property_panel_presenter.view = property_panel_view
        self.presenter_manager.scenario_panel_presenter.view = scenario_view
        self.presenter_manager.status_bar_presenter.view = status_bar_view
        self.presenter_manager.toolbar_presenter.view = toolbar_view
        attribute_panel_view.associated_presenter = self.presenter_manager.attribute_panel_presenter
        menu_bar_view.associated_presenter = self.presenter_manager.menu_bar_presenter
        property_panel_view.associated_presenter = self.presenter_manager.property_panel_presenter
        scenario_view.associated_presenter = self.presenter_manager.scenario_panel_presenter
        status_bar_view.associated_presenter = self.presenter_manager.status_bar_presenter
        toolbar_view.associated_presenter = self.presenter_manager.toolbar_presenter
        attribute_panel_view.init_ui()
        menu_bar_view.init_ui()
        property_panel_view.init_ui()
        scenario_view.init_ui()
        status_bar_view.init_ui()
        toolbar_view.init_ui()

    def __init_icon_presenter(self):
        elem_id = self.model.create_element('PV', QtCore.QPointF(250.0, 200.0))
        elem = self.model.elements[elem_id]
        elem_positions = {port:docking_ports.pos for port, docking_ports in enumerate(elem.docking_ports)}
        view = IconGroup(elem_positions, dataHandler.get_icon('pv.svg'))
        group_presenter = IconGroupPresenter(self.presenter_manager, self.model, elem_id)
        group_presenter.view = view
        view.associated_presenter = group_presenter
        group_presenter.init_scene_mapping(self.scene)
        view.init_view(self.scene)
        return group_presenter

    def __init_node_item(self, x, y):
        elem_id = self.model.create_element('PQBus', QtCore.QPointF(x, y))
        elem = self.model.elements[elem_id]
        elem_positions = {port:docking_ports.pos for port, docking_ports in enumerate(elem.docking_ports)}
        view = NodeGroup(elem_positions)
        group_presenter = NodeGroupPresenter(self.presenter_manager, self.model, elem_id)
        group_presenter.view = view
        view.associated_presenter = group_presenter
        group_presenter.init_scene_mapping(self.scene)
        view.init_view(self.scene)
        return view

    def __init_icon_item(self, x, y):
        elem_id = self.model.create_element('House', QtCore.QPointF(x, y))
        elem = self.model.elements[elem_id]
        elem_positions = {port:docking_ports.pos for port, docking_ports in enumerate(elem.docking_ports)}
        view = IconGroup(elem_positions, dataHandler.get_icon('house.svg'))
        group_presenter = IconGroupPresenter(self.presenter_manager, self.model, elem_id)
        group_presenter.view = view
        view.associated_presenter = group_presenter
        group_presenter.init_scene_mapping(self.scene)
        view.init_view(self.scene)
        return view

    def test_ep(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        ep = group_presenter.ep(group_presenter.view.icon.vp_center)
        assert isinstance(ep, ElemPort)
        assert ep.elem_id == group_presenter.elem_id
        assert ep.port == 0

    def test_vp(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        elem = self.model.elements[group_presenter.elem_id]
        test_port = elem.elem_ports()[0]
        vp = group_presenter.vp(test_port)
        assert isinstance(vp, VPoint)
        assert vp.pos == group_presenter.view.pos

    def test_raster_snap_v_points(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        for vp in group_presenter.raster_snap_v_points:
            if not isinstance(vp, VPoint):
                raise AssertionError

    def test_snap_zone(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        snap_points = group_presenter.snap_zone(group_presenter.view.icon.vp_center)
        assert len(snap_points) == 0
        node_group_1 = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        node_group_2 = self._TestGroupPresenter__init_node_item(255.0, 205.0)
        node_group_3 = self._TestGroupPresenter__init_node_item(300.0, 280.0)
        snap_points_with_items = group_presenter.snap_zone(group_presenter.view.icon.vp_center)
        for vp in snap_points_with_items:
            if not isinstance(vp, VPoint):
                raise AssertionError

        assert len(snap_points_with_items) == 2
        assert node_group_1.node.vp_center in snap_points_with_items and node_group_2.node.vp_center in snap_points_with_items and node_group_3.node.vp_center not in snap_points_with_items
        assert snap_points_with_items[0] == node_group_1.node.vp_center
        assert snap_points_with_items[1] == node_group_2.node.vp_center

    def test_can_dock(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        icon_group = self._TestGroupPresenter__init_icon_item(245.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        from_vp = group_presenter.vp(elem_port)
        can_dock_to_node = group_presenter.can_dock(from_vp, node_group.node.vp_center)
        can_dock_to_icon = group_presenter.can_dock(from_vp, icon_group.icon.vp_center)
        assert can_dock_to_node
        assert not can_dock_to_icon

    def test_to_dockables(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group_1 = self._TestGroupPresenter__init_node_item(255.0, 205.0)
        node_group_2 = self._TestGroupPresenter__init_node_item(260.0, 210.0)
        node_group_3 = self._TestGroupPresenter__init_node_item(300.0, 280.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        from_vp = group_presenter.vp(elem_port)
        snap_points = group_presenter.snap_zone(from_vp)
        to_dockables = group_presenter.to_dockables(from_vp, snap_points)
        assert len(to_dockables) == 2
        assert node_group_1.node.vp_center in to_dockables and node_group_2.node.vp_center in to_dockables and node_group_3.node.vp_center not in to_dockables
        assert to_dockables[0] == node_group_1.node.vp_center
        assert to_dockables[1] == node_group_2.node.vp_center

    def test_connectables(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group_1 = self._TestGroupPresenter__init_node_item(255.0, 205.0)
        node_group_2 = self._TestGroupPresenter__init_node_item(260.0, 210.0)
        node_group_3 = self._TestGroupPresenter__init_node_item(300.0, 280.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        snap_points = group_presenter.snap_zone(vp)
        connectables = group_presenter.connectables(snap_points, vp)
        assert len(connectables) == 2
        assert node_group_1.node.vp_center in connectables and node_group_2.node.vp_center in connectables and node_group_3.node.vp_center not in connectables
        assert connectables[0] == node_group_1.node.vp_center
        assert connectables[1] == node_group_2.node.vp_center

    def test_non_connectable(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(260.0, 210.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        snap_points = group_presenter.snap_zone(vp)
        has_non_connectables = group_presenter.non_connectable(snap_points, vp)
        assert not has_non_connectables
        icon_group = self._TestGroupPresenter__init_icon_item(255.0, 205.0)
        snap_points = group_presenter.snap_zone(vp)
        has_non_connectables_with_icon = group_presenter.non_connectable(snap_points, vp)
        assert has_non_connectables_with_icon

    def test_dock(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        group_presenter.dock(vp, node_group.node.vp_center)
        assert vp.follows(node_group.node.vp_center)

    def test_undock(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        group_presenter.dock(vp, node_group.node.vp_center)
        group_presenter.undock(vp, node_group.node.vp_center)
        assert not vp.follows(node_group.node.vp_center)

    def test_on_position_changed(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        group_presenter.dock(vp, node_group.node.vp_center)
        assert vp.follows(node_group.node.vp_center)
        group_presenter.on_position_changed(node_group.node.vp_center, QtCore.QPointF(1.0, 1.0), Change.moved, section_manager.presenter_section)
        assert vp.follows(node_group.node.vp_center)
        group_presenter.on_position_changed(vp, QtCore.QPointF(1.0, 1.0), Change.snapped, section_manager.presenter_section)
        assert vp.follows(node_group.node.vp_center)
        vp.pos += QtCore.QPointF(1.0, 1.0)
        group_presenter.on_position_changed(vp, QtCore.QPointF(1.0, 1.0), Change.moved, section_manager.presenter_section)
        assert not vp.follows(node_group.node.vp_center)

    def test_on_selection_changed(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        group_presenter.view.selected = False
        group_presenter.on_selection_changed()
        assert group_presenter.elem_id not in self.model.selection
        assert group_presenter.view.icon.z_value == 2
        for endpoint in group_presenter.view.endpoints:
            assert endpoint.z_value == 1
            if not not endpoint.visible:
                raise AssertionError

        for line in group_presenter.view.lines:
            if not line.z_value == 1:
                raise AssertionError

        group_presenter.view.selected = True
        group_presenter.on_selection_changed()
        assert group_presenter.elem_id in self.model.selection
        assert group_presenter.view.icon.z_value == 1001
        for endpoint in group_presenter.view.endpoints:
            assert endpoint.z_value == 1000
            if not endpoint.visible:
                raise AssertionError

        for line in group_presenter.view.lines:
            if not line.z_value == 1000:
                raise AssertionError

    def test_on_mouse_released(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        raster_pos_x = round(vp.pos.x() / config.RASTER_SIZE) * config.RASTER_SIZE
        raster_pos_y = round(vp.pos.y() / config.RASTER_SIZE) * config.RASTER_SIZE
        assert vp.pos.x() != raster_pos_x
        assert vp.pos.y() == raster_pos_y
        group_presenter.on_mouse_released(QtCore.QPointF(250.0, 200.0))
        assert vp.follows(node_group.node.vp_center)
        assert vp.pos.x() == raster_pos_x
        assert vp.pos.y() == raster_pos_y

    def test_on_elements(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        len_before_remove = len(self.model.elements_event)
        self.model.elements.pop(group_presenter.elem_id)
        group_presenter.on_elements()
        len_after_remove = len(self.model.elements_event)
        assert len_before_remove - len_after_remove == 1

    def test_on_positions(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[0]
        vp = group_presenter.vp(elem_port)
        self.model.set_pos(elem_port, QtCore.QPointF(240.0, 240.0))
        assert vp.pos.x() == 250.0
        assert vp.pos.y() == 200.0
        group_presenter.on_positions()
        assert vp.pos.x() == 240.0
        assert vp.pos.y() == 240.0

    def test_on_selection(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        self.model.selection.add(group_presenter.elem_id)
        group_presenter.on_selection()
        assert group_presenter.view.selected
        self.model.selection.discard(group_presenter.elem_id)
        group_presenter.on_selection()
        assert not group_presenter.view.selected

    def test_on_dockings(self):
        self._TestGroupPresenter__init_test_environment()
        group_presenter = self._TestGroupPresenter__init_icon_presenter()
        node_group = self._TestGroupPresenter__init_node_item(250.0, 200.0)
        elem = self.model.elements[group_presenter.elem_id]
        elem_port = elem.elem_ports()[1]
        vp = group_presenter.vp(elem_port)
        self.model.dock(elem_port, node_group.associated_presenter.ep(node_group.node.vp_center))
        assert not vp.follows(node_group.node.vp_center)
        group_presenter.on_dockings()
        assert vp.follows(node_group.node.vp_center)