# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/dialogs/file_chooser_dialog.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6481 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .utils import adjust_filename_to_globs, retrieve_lowercase_extension, run_dialog
import os

class FileChooserDialog(Gtk.FileChooserDialog):
    accept_responses = (
     Gtk.ResponseType.ACCEPT,
     Gtk.ResponseType.YES,
     Gtk.ResponseType.APPLY,
     Gtk.ResponseType.OK)
    persist = False

    @property
    def parser(self):
        try:
            return getattr(self.get_filter(), 'parser')
        except AttributeError:
            return

    @property
    def filename(self):
        filename = super(FileChooserDialog, self).get_filename()
        if filename is not None:
            filename = adjust_filename_to_globs(filename, self.selected_globs)
            self.set_filename(filename)
        return filename

    @property
    def selected_globs(self):
        """ Returns the extension glob corresponding to the selected filter """
        fltr = self.get_filter()
        if fltr is None:
            return
        selected_name = fltr.get_name()
        for fltr in self.filters:
            try:
                name, globs = fltr
            except TypeError:
                parser = getattr(fltr, 'parser')
                name, globs = parser.description, parser.extensions

            if selected_name == name:
                if len(globs):
                    if globs[0] != '*.*':
                        return [retrieve_lowercase_extension(glob) for glob in globs]
                return

    def __init__(self, title, action, parent=None, buttons=None, current_name=None, current_folder=os.path.expanduser('~'), extra_widget=None, filters=[], multiple=False, confirm_overwrite=True, persist=False):
        super(FileChooserDialog, self).__init__(title=title,
          action=action,
          parent=parent,
          buttons=buttons)
        self.update(multiple=multiple,
          confirm_overwrite=confirm_overwrite,
          extra_widget=extra_widget,
          filters=filters,
          current_name=current_name,
          current_folder=current_folder,
          persist=persist)

    def update(self, **kwargs):
        """ Updates the dialog with the given set of keyword arguments, 
            and then returns itself """
        if 'title' in kwargs:
            if kwargs['title'] is not None:
                self.set_title(kwargs.pop('title'))
            elif 'action' in kwargs:
                if kwargs['action'] is not None:
                    self.set_action(kwargs.pop('action'))
                else:
                    if 'parent' in kwargs:
                        if kwargs['parent'] is not None:
                            self.set_parent(kwargs.pop('parent'))
                    if 'buttons' in kwargs:
                        self.get_action_area().foreach(lambda w: w.destroy())
                        (self.add_buttons)(*kwargs.pop('buttons'))
                if 'multiple' in kwargs:
                    self.set_select_multiple(kwargs.pop('multiple'))
            else:
                if 'confirm_overwrite' in kwargs:
                    self.set_do_overwrite_confirmation(kwargs.pop('confirm_overwrite'))
                if 'extra_widget' in kwargs:
                    if kwargs['extra_widget'] is not None:
                        self.set_extra_widget(kwargs.pop('extra_widget'))
            if 'current_name' in kwargs and kwargs['current_name'] is not None:
                self.set_current_name(kwargs.pop('current_name'))
        else:
            if 'current_folder' in kwargs:
                if kwargs['current_folder'] is not None:
                    self.set_current_folder(kwargs.pop('current_folder'))
            if 'filters' in kwargs:
                for fltr in self.list_filters():
                    self.remove_filter(fltr)

                self.filters = list(kwargs.pop('filters'))
                for fltr in self._get_object_file_filters(self.filters):
                    self.add_filter(fltr)

        self.persist = kwargs.pop('persist', self.persist)
        return self

    def _get_object_file_filters(self, filters=[]):
        """ Parses a list of textual file filter globs or Gtk.FileFilter objects
         into Gtk.FileFilter objects """
        for obj in filters:
            if isinstance(obj, Gtk.FileFilter):
                yield obj
            else:
                name, re = obj
                ffilter = Gtk.FileFilter()
                ffilter.set_name(name)
                if isinstance(re, str):
                    ffilter.add_pattern(re)
                else:
                    for expr in re:
                        ffilter.add_pattern(expr)

                yield ffilter

    def run(self, *args, **kwargs):
        kwargs['destroy'] = not self.persist
        return run_dialog(self, *args, **kwargs)