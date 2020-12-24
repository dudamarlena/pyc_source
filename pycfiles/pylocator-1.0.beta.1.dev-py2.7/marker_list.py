# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/marker_list.py
# Compiled at: 2012-04-18 10:17:23
from __future__ import division
import gobject, gtk
from dialogs import edit_coordinates, edit_label_of_marker
from events import EventHandler
from colors import choose_one_color, tuple2gdkColor, gdkColor2tuple
from markers import Marker
from list_toolbar import ListToolbar
from shared import shared

class MarkerList(gtk.VBox):
    paramd = {}

    def __init__(self):
        super(MarkerList, self).__init__(self)
        self.set_homogeneous(False)
        EventHandler().attach(self)
        self._markers = {}
        self._marker_ids = {}
        self.nmrk = 0
        self.__ignore_sel_changed = False
        toolbar = self.__create_toolbar()
        self.pack_start(toolbar, False, False)
        self.emptyIndicator = gtk.Label('No marker defined')
        self.emptyIndicator.show()
        self.pack_start(self.emptyIndicator, False, False)
        self.tree_mrk = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.nmrk = 0
        self.treev_mrk = gtk.TreeView(self.tree_mrk)
        self._treev_sel = self.treev_mrk.get_selection()
        self._treev_sel.connect('changed', self.treev_sel_changed)
        self._treev_sel.set_mode(gtk.SELECTION_SINGLE)
        renderer = gtk.CellRendererText()
        renderer.set_property('xalign', 1.0)
        self.col1 = gtk.TreeViewColumn('#', renderer, text=0)
        self.treev_mrk.append_column(self.col1)
        self.col2 = gtk.TreeViewColumn('Label', renderer, text=1)
        self.treev_mrk.append_column(self.col2)
        self.col3 = gtk.TreeViewColumn('Position', renderer, text=2)
        self.treev_mrk.append_column(self.col3)
        self.scrolledwindow = gtk.ScrolledWindow()
        self.pack_start(self.scrolledwindow, True, True)
        self.scrolledwindow.add(self.treev_mrk)
        self.scrolledwindow.show()
        self.show_all()
        self.__update_treeview_visibility()

    def __create_toolbar(self):
        conf = [
         [
          gtk.STOCK_ADD,
          'Add',
          'Add new marker by entering its coordinates',
          self.cb_add],
         [
          gtk.STOCK_REMOVE,
          'Remove',
          'Remove selected marker',
          self.cb_remove],
         '-',
         [
          gtk.STOCK_GO_UP,
          'Move up',
          'Move selected marker up in list',
          self.cb_move_up],
         [
          gtk.STOCK_GO_DOWN,
          'Move down',
          'Move selected marker down in list',
          self.cb_move_down],
         '-',
         [
          gtk.STOCK_BOLD,
          'Label',
          'Edit Label of marker',
          self.cb_edit_label],
         [
          gtk.STOCK_EDIT,
          'Position',
          'Edit position of marker',
          self.cb_edit_position],
         [
          gtk.STOCK_SELECT_COLOR,
          'Color',
          'Select color for marker',
          self.cb_choose_color]]
        return ListToolbar(conf)

    def update_viewer(self, event, *args):
        if event == 'add marker':
            marker = args[0]
            self.add_marker(marker)
        elif event == 'remove marker':
            marker = args[0]
            self.remove_marker(marker)
        elif event == 'label marker':
            marker, label = args
            id_ = self._marker_ids[marker.uuid]
            treeiter = self._get_iter_for_id(id_)
            if treeiter:
                self.tree_mrk.set(treeiter, 1, str(label))
        elif event == 'move marker':
            marker, center = args
            x, y, z = center
            id_ = self._marker_ids[marker.uuid]
            treeiter = self._get_iter_for_id(id_)
            self.tree_mrk.set(treeiter, 2, self.__format_coord_string(x, y, z))
        elif event == 'select marker':
            marker = args[0]
            self.__set_marker_selected(marker, True)
        elif event == 'unselect marker':
            marker = args[0]
            self.__set_marker_selected(marker, False)

    def cb_add(self, *args):
        parent_window = self.get_parent_window()
        coordinates = edit_coordinates(description='Please enter the coordinates\nfor the marker to be added')
        if coordinates == None:
            return
        else:
            x, y, z = coordinates
            marker = Marker(xyz=(x, y, z), rgb=EventHandler().get_default_color(), radius=shared.ratio * 3)
            EventHandler().add_marker(marker)
            return

    def cb_remove(self, *args):
        marker = self.__get_selected_marker()
        EventHandler().remove_marker(marker)

    def cb_choose_color(self, *args):
        marker = self.__get_selected_marker()
        old_color = marker.get_color()
        new_color = choose_one_color('New color for marker', tuple2gdkColor(old_color))
        EventHandler().notify('color marker', marker, gdkColor2tuple(new_color))

    def cb_move_up(self, *args):
        self._move_in_list(up=True)

    def cb_move_down(self, *args):
        self._move_in_list(up=False)

    def cb_edit_label(self, *args):
        marker = self.__get_selected_marker()
        edit_label_of_marker(marker)

    def cb_edit_position(self, *args):
        marker = self.__get_selected_marker()
        x_old, y_old, z_old = marker.get_center()
        coordinates = edit_coordinates(x_old, y_old, z_old)
        if coordinates == None:
            return
        else:
            x, y, z = coordinates
            EventHandler().notify('move marker', marker, (x, y, z))
            self.treev_sel_changed(self._treev_sel)
            return

    def _move_in_list(self, up=True):
        if self._treev_sel.count_selected_rows == 0:
            return
        model, rows = self._treev_sel.get_selected_rows()
        for path1 in rows:
            if up:
                path2 = (
                 path1[0] - 1,)
            else:
                path2 = (
                 path1[0] + 1,)
            if path2[0] < 0:
                continue
            iter1 = model.get_iter(path1)
            try:
                iter2 = model.get_iter(path2)
            except ValueError:
                continue

            model.swap(iter1, iter2)

    def _get_iter_for_id(self, id_):
        treeiter = self.tree_mrk.get_iter_first()
        while treeiter:
            if self.tree_mrk.get(treeiter, 0)[0] == id_:
                break
            else:
                treeiter = self.tree_mrk.iter_next(treeiter)

        return treeiter

    def add_marker(self, marker):
        self.nmrk += 1
        self._marker_ids[marker.uuid] = self.nmrk
        self._markers[self.nmrk] = marker
        x, y, z = marker.get_center()
        treeiter = self.tree_mrk.append(None)
        self.tree_mrk.set(treeiter, 0, self.nmrk, 1, '', 2, self.__format_coord_string(x, y, z))
        self.__update_treeview_visibility()
        return

    def remove_marker(self, marker):
        try:
            try:
                id_ = self._marker_ids[marker.uuid]
                treeiter = self._get_iter_for_id(id_)
                if treeiter:
                    self.tree_mrk.remove(treeiter)
                    del self._markers[id_]
                    del self._marker_ids[marker.uuid]
            except Exception as e:
                print 'Exception in MarkerList.remove_marker'

        finally:
            self.__update_treeview_visibility()

    def treev_sel_changed(self, selection):
        if self.__ignore_sel_changed:
            return
        else:
            EventHandler().clear_selection()
            try:
                treeiter = selection.get_selected()[1]
                if treeiter:
                    mrk_id = self.tree_mrk.get(treeiter, 0)[0]
                    if mrk_id == None:
                        return
                    marker = self._markers[mrk_id]
                    EventHandler().select_new(marker)
            except:
                pass

            return

    def __update_treeview_visibility(self):
        if self.tree_mrk.get_iter_first() == None:
            self.emptyIndicator.show()
            self.scrolledwindow.hide()
        else:
            self.emptyIndicator.hide()
            self.scrolledwindow.show()
        return

    def __get_selected_marker(self):
        treeiter = self._treev_sel.get_selected()[1]
        if not treeiter:
            return
        mrk_id = self.tree_mrk.get(treeiter, 0)[0]
        return self._markers[mrk_id]

    def __format_coord_string(self, x, y, z):

        def fmt(f):
            s = '%.1f' % f
            return ' ' * (7 - len(s)) + s

        return '%s,%s,%s' % (fmt(x), fmt(y), fmt(z))

    def __set_marker_selected(self, marker, selected=True):
        id_ = self._marker_ids[marker.uuid]
        treeiter = self._get_iter_for_id(id_)
        try:
            try:
                self.__ignore_sel_changed = True
                if selected:
                    self._treev_sel.select_iter(treeiter)
                else:
                    self._treev_sel.unselect_iter(treeiter)
            except Exception:
                pass

        finally:
            self.__ignore_sel_changed = False