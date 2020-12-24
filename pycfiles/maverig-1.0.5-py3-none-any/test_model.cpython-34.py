# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_model.py
# Compiled at: 2014-10-22 13:09:59
# Size of source mod 2**32: 16232 bytes
from unittest import TestCase
from PySide import QtCore
from maverig.models.model import Model, Mode
import os
from maverig.data.components.abstractComponent import ElemPort
from maverig.utils.event import Event

class TestModel(TestCase):

    def setUp(self):
        self.model = Model()

    def test_switch_modes(self):
        """Switches between the composition modes"""
        self.model.mode = Mode.comp
        self.model.switch_modes(Mode.comp, Mode.selection)
        assert self.model.mode == Mode.selection
        self.model.switch_modes(Mode.comp, Mode.selection)
        assert self.model.mode == Mode.comp
        self.model.switch_modes(Mode.hand, Mode.selection)
        assert self.model.mode == Mode.hand

    def test_is_selectable(self):
        """Checks for an item if it is selectable or not"""
        elem_id = self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.mode = Mode.selection
        assert self.model.is_selectable(elem_id)
        self.model.mode = Mode.hand
        assert not self.model.is_selectable(elem_id)

    def test_change_history(self):
        """changes history after an action"""
        assert self.model.changes_count() == self.model.last_change_count
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        assert self.model.changes_count() != self.model.last_change_count

    def test_copy_history(self):
        """copies the history of actions"""
        assert self.model.history_temp == []
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        assert self.model.history_temp == []
        self.model.history_temp = self.model.copy_history()
        assert self.model.history_temp != []

    def test_changes_count(self):
        """summs up changes after an edit to the history"""
        assert self.model.changes_count() == 0
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        assert self.model.changes_count() == 1

    def test_copy_to_clipboard(self):
        """copies all elements of the elem_ids list to an internal clipboard"""
        assert self.model.clipboard_elements == {}
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.create_element('PV', QtCore.QPointF(300, 70))
        self.model.create_element('PV', QtCore.QPointF(200, 80))
        assert self.model.clipboard_elements == {}
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        self.model.copy_to_clipboard(self.model.selection)
        assert self.model.clipboard_elements != {}

    def test_paste_from_clipboard(self):
        """ paste all elements from internal clipboard and return the new elem_ids
        only dockings inside of clipboard will be maintained
        """
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.create_element('PV', QtCore.QPointF(300, 70))
        self.model.create_element('PV', QtCore.QPointF(200, 80))
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        self.model.copy_to_clipboard(self.model.selection)
        elem_ids = self.model.paste_from_clipboard()
        assert len(elem_ids) == 3

    def test_create_element(self):
        """creates an element"""
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        assert len(self.model.elements) == 1

    def test_delete_element(self):
        """deletes an element"""
        elem_id = self.model.create_element('PV', QtCore.QPointF(400, 60))
        assert len(self.model.elements) == 1
        self.model.delete_element(elem_id)
        assert len(self.model.elements) == 0

    def test_get_shared_params(self):
        """ return a list of composed parameter instances which are contained in each element of elem_ids
            e.g. [NumResidents(), NumHouseHolds() ...]

        - parameter.value: the parameter value of the first element of elem_ids
        - parameter.shared_values: a list of values according to each element in elem_ids """
        elem_ids = {elem_id for elem_id in self.model.elements}
        assert self.model.get_shared_params(elem_ids) == []
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.create_element('PV', QtCore.QPointF(300, 70))
        self.model.create_element('PV', QtCore.QPointF(200, 80))
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        elem_ids = self.model.selection
        shared_params = self.model.get_shared_params(elem_ids)
        assert self.model.get_shared_params(elem_ids) != []

    def test_get_param_value(self):
        """ get value of parameter with param_name in element elem_id
        return None if param_name does not exist"""
        elem_ids = {elem_id for elem_id in self.model.elements}
        assert self.model.get_shared_params(elem_ids) == []
        pv_1 = self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.set_param_value(pv_1, 'datafile', os.path.normpath('maverig/tests/data/pv_30kw.small.csv'))
        pv_2 = self.model.create_element('PV', QtCore.QPointF(450, 30))
        self.model.set_param_value(pv_2, 'datafile', os.path.normpath('maverig/tests/data/pv_30kw.small.csv'))
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        elem_ids = self.model.selection
        for id in elem_ids:
            assert self.model.get_param_value(id, 'datafile') == os.path.normpath('maverig/tests/data/pv_30kw.small.csv')
            if not self.model.get_param_value(id, 'other') is None:
                raise AssertionError

    def test_set_param_value(self):
        """ set value of parameter with param_name in element elem_id
        if value is not None"""
        elem_ids = {elem_id for elem_id in self.model.elements}
        assert self.model.get_shared_params(elem_ids) == []
        pv_1 = self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.set_param_value(pv_1, 'datafile', os.path.normpath('maverig/tests/data/pv_30kw.small.csv'))
        pv_2 = self.model.create_element('PV', QtCore.QPointF(450, 30))
        self.model.set_param_value(pv_2, 'datafile', os.path.normpath('maverig/tests/data/pv_30kw.small.csv'))
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        elem_ids = self.model.selection
        for id in elem_ids:
            assert self.model.get_param_value(id, 'datafile') == os.path.normpath('maverig/tests/data/pv_30kw.small.csv')
            if not self.model.get_param_value(id, 'other') is None:
                raise AssertionError

    def test_get_selected(self):
        """ get value of parameter with param_name in element elem_id
        return None if param_name does not exist"""
        self.model.create_element('PV', QtCore.QPointF(400, 60))
        self.model.selection = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        elem_ids = self.model.selection
        for id in elem_ids:
            if not self.model.get_selected(id) is True:
                raise AssertionError

    def test_set_selected(self):
        """sets selected-flag to marked elements"""
        el1 = self.model.create_element('PV', QtCore.QPointF(400, 60))
        el2 = self.model.create_element('PV', QtCore.QPointF(300, 70))
        elem_ids = {elem_id for elem_id in self.model.elements if self.model.is_selectable(elem_id)}
        self.model.update()
        for id in elem_ids:
            self.model.set_selected(id, elem_ids)

        el3 = self.model.create_element('PV', QtCore.QPointF(340, 40))
        self.model.update()
        assert self.model.get_selected(el1) is True
        assert self.model.get_selected(el2) is True
        assert self.model.get_selected(el3) is False

    def test_docking_port(self):
        """get the docking_port of an element"""
        elem_id = self.model.create_element('PV', QtCore.QPointF(400, 60))
        elem = self.model.elements[elem_id]
        for ep in elem.elem_ports():
            assert self.model.docking_port(ep).dockings_out == {}
            if not self.model.docking_port(ep).dockings_in == {}:
                raise AssertionError

    def test_get_pos(self):
        """get the position of an element"""
        elem_id = self.model.create_element('PV', QtCore.QPointF(400, 60))
        elem = self.model.elements[elem_id]
        for ep in elem.elem_ports():
            if not self.model.get_pos(ep) == QtCore.QPointF(400, 60):
                raise AssertionError

    def test_set_pos(self):
        """set the position of an element"""
        elem_id = self.model.create_element('PV', QtCore.QPointF(400, 60))
        elem = self.model.elements[elem_id]
        for ep in elem.elem_ports():
            if not self.model.get_pos(ep) == QtCore.QPointF(400, 60):
                raise AssertionError

        for ep in elem.elem_ports():
            self.model.set_pos(ep, QtCore.QPointF(300, 50))

        for ep in elem.elem_ports():
            if not self.model.get_pos(ep) == QtCore.QPointF(300, 50):
                raise AssertionError

    def test_dockings_out(self):
        """ return an array of outgoing element ports """
        refbus_1 = self.model.create_element('RefBus', QtCore.QPointF(200, 15))
        branch_1 = self.model.create_element('Branch', QtCore.QPointF())
        bus_1 = self.model.create_element('PQBus', QtCore.QPointF(300, 60))
        self.model.elements[branch_1].docking_ports[0].pos = QtCore.QPointF(200, 15)
        self.model.elements[branch_1].docking_ports[1].pos = QtCore.QPointF(300, 60)
        self.model.dock(ElemPort(bus_1, 0), ElemPort(branch_1, 1))
        self.model.dock(ElemPort(branch_1, 0), ElemPort(refbus_1, 0))
        branch_elem = self.model.elements[branch_1]
        assert branch_elem.elem_ports()[0] == ElemPort(elem_id='Branch_2', port=0)
        assert branch_elem.elem_ports()[1] == ElemPort(elem_id='Branch_2', port=1)
        assert self.model.dockings_in(branch_elem.elem_ports()[0]) == []
        assert self.model.dockings_out(branch_elem.elem_ports()[0]) == [ElemPort(elem_id='RefBus_1', port=0)]
        assert self.model.dockings_in(branch_elem.elem_ports()[1]) == [ElemPort(elem_id='PQBus_3', port=0)]
        assert self.model.dockings_out(branch_elem.elem_ports()[1]) == []

    def test_dockings_in(self):
        """ return an array of outgoing element ports """
        refbus_1 = self.model.create_element('RefBus', QtCore.QPointF(200, 15))
        branch_1 = self.model.create_element('Branch', QtCore.QPointF())
        bus_1 = self.model.create_element('PQBus', QtCore.QPointF(300, 60))
        self.model.elements[branch_1].docking_ports[0].pos = QtCore.QPointF(200, 15)
        self.model.elements[branch_1].docking_ports[1].pos = QtCore.QPointF(300, 60)
        self.model.dock(ElemPort(bus_1, 0), ElemPort(branch_1, 1))
        self.model.dock(ElemPort(branch_1, 0), ElemPort(refbus_1, 0))
        branch_elem = self.model.elements[branch_1]
        assert branch_elem.elem_ports()[0] == ElemPort(elem_id='Branch_2', port=0)
        assert branch_elem.elem_ports()[1] == ElemPort(elem_id='Branch_2', port=1)
        assert self.model.dockings_in(branch_elem.elem_ports()[0]) == []
        assert self.model.dockings_out(branch_elem.elem_ports()[0]) == [ElemPort(elem_id='RefBus_1', port=0)]
        assert self.model.dockings_in(branch_elem.elem_ports()[1]) == [ElemPort(elem_id='PQBus_3', port=0)]
        assert self.model.dockings_out(branch_elem.elem_ports()[1]) == []

    def test_can_dock(self):
        """tests if one component may dock to another"""
        refbus_1 = self.model.create_element('RefBus', QtCore.QPointF(200, 15))
        refbus_1_elem = self.model.elements[refbus_1]
        branch_1 = self.model.create_element('Branch', QtCore.QPointF())
        branch_1_elem = self.model.elements[branch_1]
        bus_1 = self.model.create_element('PQBus', QtCore.QPointF(300, 60))
        bus_1_elem = self.model.elements[bus_1]
        assert self.model.can_dock(branch_1_elem.elem_ports()[0], refbus_1_elem.elem_ports()[0]) is True
        assert self.model.can_dock(refbus_1_elem.elem_ports()[0], bus_1_elem.elem_ports()[0]) is False

    def test_dock(self):
        """docks branch elements to other elements, if allowed"""
        refbus_1 = self.model.create_element('RefBus', QtCore.QPointF(200, 15))
        branch_1 = self.model.create_element('Branch', QtCore.QPointF())
        bus_1 = self.model.create_element('PQBus', QtCore.QPointF(300, 60))
        self.model.elements[branch_1].docking_ports[0].pos = QtCore.QPointF(200, 15)
        self.model.elements[branch_1].docking_ports[1].pos = QtCore.QPointF(300, 60)
        self.model.dock(ElemPort(bus_1, 0), ElemPort(branch_1, 1))
        self.model.dock(ElemPort(branch_1, 0), ElemPort(refbus_1, 0))
        branch_elem = self.model.elements[branch_1]
        assert branch_elem.elem_ports()[0] == ElemPort(elem_id='Branch_2', port=0)
        assert branch_elem.elem_ports()[1] == ElemPort(elem_id='Branch_2', port=1)
        assert self.model.dockings_in(branch_elem.elem_ports()[0]) == []
        assert self.model.dockings_out(branch_elem.elem_ports()[0]) == [ElemPort(elem_id='RefBus_1', port=0)]
        assert self.model.dockings_in(branch_elem.elem_ports()[1]) == [ElemPort(elem_id='PQBus_3', port=0)]
        assert self.model.dockings_out(branch_elem.elem_ports()[1]) == []

    def test_undock(self):
        """undocks docked components"""
        refbus_1 = self.model.create_element('RefBus', QtCore.QPointF(200, 15))
        branch_1 = self.model.create_element('Branch', QtCore.QPointF())
        bus_1 = self.model.create_element('PQBus', QtCore.QPointF(300, 60))
        self.model.elements[branch_1].docking_ports[0].pos = QtCore.QPointF(200, 15)
        self.model.elements[branch_1].docking_ports[1].pos = QtCore.QPointF(300, 60)
        self.model.dock(ElemPort(bus_1, 0), ElemPort(branch_1, 1))
        self.model.dock(ElemPort(branch_1, 0), ElemPort(refbus_1, 0))
        self.model.undock(ElemPort(bus_1, 0), ElemPort(branch_1, 1))
        self.model.undock(ElemPort(branch_1, 0), ElemPort(refbus_1, 0))
        branch_elem = self.model.elements[branch_1]
        assert branch_elem.elem_ports()[0] == ElemPort(elem_id='Branch_2', port=0)
        assert branch_elem.elem_ports()[1] == ElemPort(elem_id='Branch_2', port=1)
        assert self.model.dockings_in(branch_elem.elem_ports()[0]) == []
        assert self.model.dockings_out(branch_elem.elem_ports()[0]) == []
        assert self.model.dockings_in(branch_elem.elem_ports()[1]) == []
        assert self.model.dockings_out(branch_elem.elem_ports()[1]) == []

    def test_update(self):
        """ fires all events with pending demands """
        self.counter = 0

        def on_elements():
            self.counter += 1

        self.model.update()
        assert self.counter == 0
        self.model.dockings_event += on_elements
        self.model.dockings_event.demand()
        self.model.update()
        assert self.counter == 1

    def test_update_all(self):
        """ fires all events """
        self.counter = 0

        def on_elements():
            self.counter += 1

        self.model.update()
        assert self.counter == 0
        self.model.dockings_event += on_elements
        self.model.elements_event += on_elements
        self.model.positions_event += on_elements
        self.model.dockings_event.demand()
        self.model.update()
        assert self.counter == 1
        self.model.elements_event.demand()
        self.model.update()
        assert self.counter == 2
        self.model.positions_event.demand()
        self.model.elements_event.demand()
        self.model.update()
        assert self.counter == 4