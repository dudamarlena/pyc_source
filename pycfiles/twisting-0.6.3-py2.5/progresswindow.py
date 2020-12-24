# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/gui_worker/progresswindow.py
# Compiled at: 2009-03-29 13:01:35
"""Useful window for  progress task boxes display and management.
"""
import gtk
from gtk.gdk import keyval_name
from zope.interface import implements
from twisting import IProgress, ProgressBase, NotInitializeError
from twisting.gui_worker import ProgressBox, TaskBox
from twisting.tools import get_filepath
import logging
log = logging.getLogger()
__all__ = [
 'ProgressWindow']

class ProgressWindow(ProgressBase):
    """Specific gtk window for task boxes from the twisting API management.
    """
    implements(IProgress)

    def __init__(self, title='Progression dialog', all_finish_callback=None):
        """Instantiate a new singleton window that can be call everywhere
        after. Init main quit callback, variable and call gtk widgets building
        method.

        @param title: title of the windows, default: 'Progression dialog'
        @type title: str

        @param all_finish_callback: specific callback for all tasks ending
        @type all_finish_callback: function
        """
        ProgressBase.__init__(self, all_finish_callback=all_finish_callback)
        self.parent = None
        self.progress_bar = None
        self.progress_box = None
        self.__separator_dict = dict()
        self.reset(title)
        return

    def reset(self, title='Progression dialog'):
        """
        """
        self.__init_widgets(title)
        self.__init_callbacks()
        if len(self.task_dict) > 0:
            for key_ in self.task_dict.keys():
                task_ = self.task_dict[key_]
                separator_ = self.__separator_dict[key_]
                self.__mainbox.pack_start(task_, expand=False, fill=False)
                self.__mainbox.pack_start(separator_, expand=False, fill=False)
                self.window.show_all()

    def set_parent(self, parent, progress_bar=None):
        """Update the parent window for quit management and progress box to
        update when the pulse method is called.

        @param parent: parent window
        @type parent: gtk.Window

        @param progress_bar: gtk progress bar from the parent to update
        @type progress_bar: gtk.ProgressBar
        """
        self.window.set_transient_for(parent)
        self.window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.window.set_destroy_with_parent(True)
        self.parent = parent
        if progress_bar:
            self.progress_box = ProgressBox(progress_bar)

    def set_progress_box(self, progress_bar):
        """
        @param progress_bar: gtk progress bar from the parent to update
        @type progress_bar: gtk.ProgressBar
        """
        self.progress_box = ProgressBox(progress_bar)

    def set_progress_bar(self, progress_bar):
        """Easy method to set a new progress bar callback. Useful when you
        change your main window.
        """
        self.progress_box.progress_bar = progress_bar

    def __init_widgets(self, title):
        """Init the worker progress window style.
        """
        self.window = gtk.Window()
        self.window.set_resizable(True)
        self.window.resize(420, 280)
        self.window.set_deletable(False)
        self.window.set_destroy_with_parent(True)
        self.window.set_title(title)
        if self.parent:
            self.set_parent(self.parent, self.progress_bar)
        self.__mainbox = gtk.VBox()
        self.__mainbox.pack_end(gtk.VBox(), padding=20)
        event_box = gtk.EventBox()
        color = gtk.gdk.color_parse('#FFFFFF')
        event_box.modify_bg(gtk.STATE_NORMAL, color)
        event_box.add(self.__mainbox)
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled_window.add_with_viewport(event_box)
        hide_image = gtk.Image()
        hide_file_path = get_filepath(__name__, '/static/hide_small.png')
        hide_image.set_from_file(hide_file_path)
        label = gtk.Label('Hide')
        hide_box = gtk.HBox()
        hide_box.pack_start(hide_image)
        hide_box.pack_start(label)
        self.hide_button = gtk.Button()
        self.hide_button.set_relief(gtk.RELIEF_HALF)
        self.hide_button.add(hide_box)
        buttonbox = gtk.HButtonBox()
        buttonbox.set_property('layout-style', gtk.BUTTONBOX_END)
        buttonbox.pack_start(self.hide_button)
        borderbox = gtk.VBox()
        borderbox.set_border_width(5)
        borderbox.pack_start(scrolled_window)
        borderbox.pack_start(buttonbox, expand=False, fill=False, padding=4)
        self.window.add(borderbox)

    def __init_callbacks(self):
        """Set the pre-define callbacks.
        """
        self.hide_button.connect('clicked', self.__on_hide)
        self.window.connect('destroy', self.__on_quit)

    def show(self):
        """Show window wrapping to show the progess window.
        """
        if not self.window:
            self.reset()
        self.window.show_all()
        self.window.present()

    def __on_hide(self, widget):
        """Hide gui callback.
        """
        self.window.hide()

    def hide(self):
        """Show window wrapping to hide the progess window.
        """
        if not self.window:
            return
        self.window.hide()
        if self.parent:
            self.parent.present()

    def __on_quit(self, widget):
        """Quit gui callback.
        """
        self.window = None
        self.quit()
        return

    def add_task(self, id_, pretty_name):
        """Add a new task box into the progress window and init the twisted
        *deferToThread* callbacks for work, error, and result.

        @param id_: id of the task to create
        @type id_: str

        @param pretty_name: pretty name of the task to display in the box
        @type pretty_name: str
        """
        if not hasattr(self, 'initialized'):
            msg = 'You should initialize the progress window before using it'
            raise NotInitializeError(msg)
        if self.task_dict.has_key(id_):
            return True
        task_ = TaskBox(id_, pretty_name, self.remove_task, self.task_finish)
        self.__mainbox.pack_start(task_, expand=False, fill=False)
        separator = gtk.HSeparator()
        self.__mainbox.pack_start(separator, expand=False, fill=False)
        self.window.show_all()
        self.task_dict[id_] = task_
        self.__separator_dict[id_] = separator
        return False

    def remove_task(self, id_):
        """Remove a task box and the corresponding separator (pure esthetic
        problem, no functional need).

        @param id_: id of the task to remove
        @type id_: str
        """
        if not self.task_dict.has_key(id_):
            return
        task = self.task_dict[id_]
        ProgressBase.remove_task(self, id_)
        self.__mainbox.remove(task)
        separator = self.__separator_dict[id_]
        self.__mainbox.remove(separator)
        self.__separator_dict.pop(id_)
        self.__update_progress_box()

    def pulse(self, id_):
        """update a task box progress pulse status.

        @param id_: id of the task to update
        @type id_: str
        """
        ProgressBase.pulse(self, id_)
        self.__update_progress_box()

    def task_finish(self, id_):
        """Set the final status for a specific method and check if all tasks
        are finished. If all task are ended call the all_task_finished callback
        from the parent window.

        @param id_: id of the task that was just ended
        @type id_: str
        """
        ProgressBase.task_finish(self, id_)
        self.__update_progress_box(end_task=True)

    def __update_progress_box(self, end_task=False):
        """Refresh the progress box pulse status of the parent.
        """
        if not self.progress_box:
            return
        if len(self.task_dict) == 0:
            self.progress_box.pulse()
            return
        fraction = 0
        nb_of_active_task = 0
        pulse_only_ = False
        for key in self.task_dict.keys():
            taskbox = self.task_dict[key]
            if not taskbox.is_finished:
                if taskbox.max_pulse > 1:
                    fraction += taskbox.get_fraction()
                    nb_of_active_task += 1
                else:
                    pulse_only_ = True
                    break

        if pulse_only_ == True:
            self.progress_box.pulse(pulse_only=True)
            return
        elif nb_of_active_task > 0:
            self.progress_box.pulse(fraction, nb_of_active_task, end_task)
        else:
            self.progress_box.pulse(1, 1)

    def __on_key_press(self, widget, event):
        """Catch the buttton enter press event or escape. Not used at the
        moment, may be one day :!).
        """
        if keyval_name(event.keyval) == 'Return':
            pass
        if keyval_name(event.keyval) == 'Escape':
            pass