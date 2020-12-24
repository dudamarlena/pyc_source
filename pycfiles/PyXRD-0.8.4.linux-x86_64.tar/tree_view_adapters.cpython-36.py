# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/tree_view_adapters.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6221 bytes
import logging
logger = logging.getLogger(__name__)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ..abstract_adapter import AbstractAdapter

def wrap_property_to_treemodel_type(model, prop, treemodel_type):
    prop_value = getattr(model, prop.label)
    if not isinstance(prop_value, Gtk.TreeModel):
        wrapper = getattr(model, '__%s_treemodel_wrapper' % prop.label, None)
        if wrapper is None or not wrapper.is_wrapping(model, prop.label):
            wrapper = treemodel_type(model, prop)
        setattr(model, '__%s_treemodel_wrapper' % prop.label, wrapper)
        prop_value = wrapper
    return prop_value


def wrap_treenode_property_to_treemodel(model, prop):
    """
        Convenience function that (sparsely) wraps a TreeNode property
        to an ObjectTreeStore. If the property is a Gtk.TreeModel instance,
        it returns it without wrapping.
    """
    from .treemodels import ObjectTreeStore
    return wrap_property_to_treemodel_type(model, prop, ObjectTreeStore)


def wrap_list_property_to_treemodel(model, prop):
    """
        Convenience function that (sparsely) wraps a list property
        to an ObjectListStore. If the property is an Gtk.TreeModel instance,
        it returns it without wrapping.
    """
    from .treemodels import ObjectListStore
    return wrap_property_to_treemodel_type(model, prop, ObjectListStore)


def wrap_xydata_to_treemodel(model, prop):
    """
        Convenience function that (sparsely) wraps an XYData model
        to an XYListStore. If the property is an Gtk.TreeModel instance,
        it returns it without wrapping.
    """
    from .treemodels import XYListStore
    return wrap_property_to_treemodel_type(model, prop, XYListStore)


class AbstractTreeViewAdapter(AbstractAdapter):
    __doc__ = '\n        Abstract base class for the ObjectTreeViewAdapter and\n        XYTreeViewAdapter.\n    '
    toolkit = 'gtk'
    _check_widget_type = Gtk.TreeView
    _signal = 'changed'

    def __init__(self, controller, prop, widget):
        super(AbstractTreeViewAdapter, self).__init__(controller, prop, widget)
        if self._check_widget_type is not None:
            widget_type = type(widget)
            if not isinstance(widget, self._check_widget_type):
                raise TypeError("A '%s' can only be used for (a subclass of) a '%s' widget, and not for a '%s'!" % (
                 type(self), self._check_widget_type, widget_type))
        self._connect_widget()

    def _connect_widget(self):
        self._widget.set_model(self._treestore)
        setup = getattr(self._controller, 'setup_%s_tree_view' % self._prop.label, None)
        if callable(setup):
            setup(self._treestore, self._widget)
        else:
            logger.error("Could not find setup callable for tree view widget '%s' adapted to '%s'" % (
             self._widget,
             self._prop.label))

    def _disconnect_widget(self, widget=None):
        self._widget.set_model(None)

    def _connect_model(self):
        pass

    def _disconnect_model(self, model=None):
        pass

    def _read_widget(self):
        pass

    def _write_widget(self, val):
        pass

    def _read_property(self, *args):
        pass

    def _write_property(self, value, *args):
        pass


class ObjectListViewAdapter(AbstractTreeViewAdapter):
    __doc__ = '\n        An adapter for a TreeView widget, representing a list of objects.\n    '
    widget_types = [
     'object_list_view']

    def __init__(self, controller, prop, widget):
        assert hasattr(prop, 'data_type'), "ObjectTreeViewAdapter requires the 'data_type' attribute to be set on the property descriptor.\n" + "Controller: '%s', Model: '%s', Property: '%s'" % (controller, controller.model, prop.label)
        self._treestore = wrap_list_property_to_treemodel(controller.model, prop)
        super(ObjectListViewAdapter, self).__init__(controller, prop, widget)


class XYListViewAdapter(AbstractTreeViewAdapter):
    __doc__ = '\n        An adapter for a TreeView widget, representing an XYData model.\n    '
    widget_types = [
     'xy_list_view']

    def __init__(self, controller, prop, widget):
        self._treestore = wrap_xydata_to_treemodel(controller.model, prop)
        super(XYListViewAdapter, self).__init__(controller, prop, widget)


class ObjectTreeViewAdapter(AbstractTreeViewAdapter):
    __doc__ = '\n        An adapter for a TreeView widget, representing a tree of objects.\n    '
    widget_types = [
     'object_tree_view']

    def __init__(self, controller, prop, widget):
        self._treestore = wrap_treenode_property_to_treemodel(controller.model, prop)
        super(ObjectTreeViewAdapter, self).__init__(controller, prop, widget)