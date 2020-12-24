# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/test/test_editor.py
# Compiled at: 2016-10-03 09:39:22
import os
from bauble.editor import GenericEditorView
import bauble.prefs as prefs, bauble.paths as paths, bauble.utils as utils
from bauble.test import BaubleTestCase

class BaubleTests(BaubleTestCase):

    def test_create_generic_view(self):
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        view = GenericEditorView(filename)
        print type(view.widgets)
        self.assertTrue(type(view.widgets) is utils.BuilderWidgets)

    def test_set_title_ok(self):
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        view = GenericEditorView(filename, root_widget_name='main_window')
        title = 'testing'
        view.set_title(title)
        self.assertEquals(view.get_window().get_title(), title)

    def test_set_title_no_root(self):
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        view = GenericEditorView(filename)
        title = 'testing'
        self.assertRaises(NotImplementedError, view.set_title, title)
        self.assertRaises(NotImplementedError, view.get_window)

    def test_set_icon_no_root(self):
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        view = GenericEditorView(filename)
        title = 'testing'
        self.assertRaises(NotImplementedError, view.set_icon, title)

    def test_add_widget(self):
        import gtk
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        view = GenericEditorView(filename)
        label = gtk.Label('testing')
        view.widget_add('statusbar', label)


class PleaseIgnoreMe:
    """these cannot be tested in a non-windowed environment
    """

    def test_set_accept_buttons_sensitive_not_set(self):
        """it is a task of the presenter to indicate the accept buttons"""
        filename = os.path.join(paths.lib_dir(), 'connmgr.glade')
        view = GenericEditorView(filename, root_widget_name='main_dialog')
        self.assertRaises(AttributeError, view.set_accept_buttons_sensitive, True)

    def test_set_sensitive(self):
        filename = os.path.join(paths.lib_dir(), 'connmgr.glade')
        view = GenericEditorView(filename, root_widget_name='main_dialog')
        view.widget_set_sensitive('cancel_button', True)
        self.assertTrue(view.widgets.cancel_button.get_sensitive())
        view.widget_set_sensitive('cancel_button', False)
        self.assertFalse(view.widgets.cancel_button.get_sensitive())

    def test_set_visible_get_visible(self):
        filename = os.path.join(paths.lib_dir(), 'connmgr.glade')
        view = GenericEditorView(filename, root_widget_name='main_dialog')
        view.widget_set_visible('noconnectionlabel', True)
        self.assertTrue(view.widget_get_visible('noconnectionlabel'))
        self.assertTrue(view.widgets.noconnectionlabel.get_visible())
        view.widget_set_visible('noconnectionlabel', False)
        self.assertFalse(view.widget_get_visible('noconnectionlabel'))
        self.assertFalse(view.widgets.noconnectionlabel.get_visible())