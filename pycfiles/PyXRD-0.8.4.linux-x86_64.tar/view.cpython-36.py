# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/view.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 8139 bytes
from .support.exceptions import ViewError
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
Builder = Gtk.Builder

class View(object):
    top = None
    builder = None

    def __init__(self, top=None, parent=None, builder=None, *args, **kwargs):
        """
        Only the first three may be given as positional arguments. If an
        argument is empty a class attribute of the same name is used. This
        does not work for *parent*.

        *builder* is a path to a Glade XML file.

        *top* is a string containing the name of our top level widget.

        *parent* is used to call :meth:`set_parent_view`.

        The last two only work if *builder* is used, not if you
        intend to create widgets later from code.
        """
        (super(View, self).__init__)(*args, **kwargs)
        self.manualWidgets = {}
        self.autoWidgets = {}
        self._View__autoWidgets_calculated = False
        if top:
            self._top = top
        else:
            self._top = self.top
        if builder:
            _builder = builder
        else:
            _builder = self.builder
        if _builder is not None:
            if isinstance(_builder, Builder):
                self._builder = _builder
            else:
                self._builder = Gtk.Builder()
                self._builder.add_from_file(_builder)
        else:
            self._builder = None
        if parent is not None:
            self.set_parent_view(parent)

    def __getitem__(self, key):
        """
        Return the widget named *key*, or ``None``.
        
        .. note::
        
           In future versions this will likely change to raise ``KeyError``.
        """
        wid = None
        if key in self.manualWidgets:
            wid = self.manualWidgets[key]
        if wid is None:
            if key in self.autoWidgets:
                wid = self.autoWidgets[key]
            elif wid is None:
                if self._builder is not None:
                    wid = self._builder.get_object(key)
                    if wid is not None:
                        self.autoWidgets[key] = wid
        return wid

    def __setitem__(self, key, wid):
        """
        Add a widget. This overrides widgets of the same name that were loaded
        from XML. It does not affect GTK container/child relations.
        
        If no top widget is known, this sets it.
        """
        self.manualWidgets[key] = wid

    def show(self):
        """
        Call `show()` on each top widget or `show_all()` if only one is known. 
        Otherwise does nothing.
        """
        top = self.get_top_widget()
        if type(top) in (list, tuple):
            for t in top:
                if t is not None:
                    t.show()

        elif top is not None:
            top.show_all()

    def hide(self):
        """
        Call `hide()` on all known top widgets.
        """
        top = self.get_top_widget()
        if type(top) in (list, tuple):
            for t in top:
                if t is not None:
                    t.hide()

        elif top is not None:
            top.hide()

    def get_top_widget(self):
        return self[self._top]

    def set_parent_view(self, parent_view):
        """
        Set ``self.``:meth:`get_top_widget` transient for 
        ``parent_view.get_top_widget()``.
        """
        top = self.get_top_widget()
        if type(top) in (list, tuple):
            for t in top:
                if t is not None and hasattr(t, 'set_transient_for'):
                    t.set_transient_for(parent_view.get_top_widget())

        elif top is not None:
            if hasattr(top, 'set_transient_for'):
                top.set_transient_for(parent_view.get_top_widget())

    def set_transient(self, transient_view):
        """
        Set ``transient_view.get_top_widget()`` transient for
        ``self.``:meth:`get_top_widget`.
        """
        top = self.get_top_widget()
        if type(top) in (list, tuple):
            for t in top:
                if t is not None:
                    transient_view.get_top_widget().set_transient_for(t)

        elif top is not None:
            transient_view.get_top_widget().set_transient_for(top)

    def _custom_widget_create(self, glade, function_name, widget_name, str1, str2, int1, int2):
        if function_name is not None:
            handler = getattr(self, function_name, None)
            if handler is not None:
                return handler(str1, str2, int1, int2)

    def __iter__(self):
        """
        Return an iterator over widgets added with :meth:`__setitem__` and
        those loaded from XML.
        
        .. note::
           In case of name conflicts this yields widgets that are not 
           accessible via :meth:`__getitem__`.
        """
        self._View__extract_autoWidgets()
        import itertools
        for i in itertools.chain(self.manualWidgets, self.autoWidgets):
            yield i

    def __extract_autoWidgets(self):
        """Extract autoWidgets map if needed, out of the glade
        specifications and gtk builder"""
        if self._View__autoWidgets_calculated:
            return
        if self._builder is not None:
            for wid in self._builder.get_objects():
                try:
                    name = Gtk.Buildable.get_name(wid)
                except TypeError:
                    continue

                if name in self.autoWidgets:
                    if self.autoWidgets[name] != wid:
                        raise ViewError("Widget '%s' in builder also found in glade specification" % name)
                self.autoWidgets[name] = wid

        self._View__autowidgets_calculated = True