# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/gui_worker/taskbox.py
# Compiled at: 2009-03-29 13:01:35
"""Gui box managed by the progress window for a task progress information
presentation.
"""
from Queue import Queue
from twisted.internet import reactor
from zope.interface import implements
import gtk
from gtk.gdk import keyval_name
from twisting import ITask, TaskBase
from twisting.messages import Pause, Play, Stop
from twisting.tools import get_filepath
__all__ = [
 'TaskBox']

class TaskBox(TaskBase, gtk.EventBox):
    """Gtk event box to be added in the progress window for task progress view.
    """
    implements(ITask)

    def __init__(self, id_, pretty_name, remove_callback, finish_callback, icon='gears_medium'):
        """Init the task box variables and call init widget method to create
        and set an nice gtk event box for the progress representation of a
        specific task.

        @param id_: specific id of the task, common in all the twisting
        framework for separated management in the progress window
        @type id_: str

        @param pretty_name: much pretty name than the id, only use for gtk
        rendering and information displaying.
        @type pretty_name: str

        @param remove_callback: callback from the parent progress window
        to call on remove signal to ask for self removal when ask by the user
        @type remove_callback: function

        @param finish_callback: callback from the parent progress window
        to call at then end for main progress status update
        @type finish_callback: function

        @param icon: picto, gears representing a task work by default, can be
        overrided by other picto to and in the static img folder for other task
        type like pdf, sql...
        @type icon: str
        """
        TaskBase.__init__(self, id_, pretty_name, remove_callback, finish_callback)
        gtk.EventBox.__init__(self)
        self.__can_draw = True
        self.__progress_bar = None
        self.__progression_label = None
        self.__task_image = None
        self.play_button = None
        self.stop_button = None
        self.remove_button = None
        self.__init_widgets()
        self.set_icon(icon)
        self.__init_callbacks()
        return

    def __get_image(self, image_name):
        """Common internal method to obtain a gtk image from
        """
        file_path = get_filepath(__name__, '/static/%s.png' % image_name)
        if file_path:
            image = gtk.Image()
            image.set_from_file(file_path)
            return image
        else:
            return
        return

    def __get_progress_button(self, image_name):
        """Generic method to init a progress button with the corresponding
        image.
        """
        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        image = self.__get_image(image_name)
        if image:
            button.set_image(image)
        return button

    def __init_progress_box(self):
        """Format a progress box with default values for the task box.
        """
        progressbox = gtk.VBox()
        self.__progression_title = gtk.Label()
        self.__progression_title.set_markup('<b>%s</b>' % self.pretty_name)
        self.__progression_title.set_property('xalign', 0)
        self.__progression_title.set_property('yalign', 0)
        progressbox.pack_start(self.__progression_title, expand=True, fill=False)
        self.__progress_bar = gtk.ProgressBar()
        self.__progress_bar.set_fraction(0)
        progressbox.pack_start(self.__progress_bar, expand=True, fill=False)
        self.__progression_label = gtk.Label()
        self.__progression_label.set_markup('')
        self.__progression_label.set_property('xalign', 0)
        self.__progression_label.set_property('yalign', 1)
        progressbox.pack_start(self.__progression_label, expand=True, fill=False)
        return progressbox

    def set_icon(self, icon):
        """Public method to modify the taskbox icon on fly. The corresponding file must be placed in the twisting package.

        """
        gears_file_path = get_filepath(__name__, '/static/%s.png' % icon)
        if not gears_file_path:
            gears_file_path = get_filepath(__name__, '/static/gears_medium.png' % icon)
        self.__task_image.set_from_file(gears_file_path)

    def __init_widgets(self):
        """Init the gtk widgets from scratch to obtain the nice task box.

        @param icon: icon nam to use for nicer progress small description
        @type icon: str
        """
        color = gtk.gdk.color_parse('#EAEAEA')
        self.modify_bg(gtk.STATE_NORMAL, color)
        h_box = gtk.HBox()
        h_box.set_border_width(4)
        self.__task_image = gtk.Image()
        h_box.pack_start(self.__task_image, expand=False, fill=False, padding=10)
        progressbox = self.__init_progress_box()
        h_box.pack_start(progressbox, expand=True, fill=True, padding=10)
        self.play_button = self.__get_progress_button('pause_very_small')
        h_box.pack_start(self.play_button, expand=False, fill=False)
        self.stop_button = self.__get_progress_button('stop_very_small')
        h_box.pack_start(self.stop_button, expand=False, fill=False)
        self.remove_button = self.__get_progress_button('cross_very_small')
        h_box.pack_start(self.remove_button, expand=False, fill=False)
        self.add(h_box)
        self.show_all()

    def __init_callbacks(self):
        """
        """
        self.play_button.connect('clicked', self.on_play)
        self.connect('destroy', self.on_stop)
        self.stop_button.connect('clicked', self.on_stop)
        self.remove_button.connect('clicked', self.on_remove)

    def pulse(self):
        """Increment the progress status, get the progress info and update
        all the gtk components used for progress status view.
        """
        if TaskBase.pulse(self):
            if self.max_pulse > 1:
                fraction_ = self.get_fraction() + self.fraction_step
                self.__progress_bar.set_fraction(fraction_)
            else:
                self.__progress_bar.set_pulse_step(self.fraction_step)
                self.__progress_bar.pulse()
            return True
        else:
            self.__progress_bar.set_fraction(1)
            self.play_button.set_sensitive(False)
            self.stop_button.set_sensitive(False)
            return False

    def set_progress_end_state(self, label):
        """Common internal terminal method call from stop or finish for gtk
        and finish flag update.

        @param label: specific label to display at the task end
        @type label: str
        """
        TaskBase.set_progress_end_state(self, label)
        if self.__can_draw:
            self.__progress_bar.set_fraction(1)
            self.set_text(label)
        self.stop_button.set_sensitive(False)
        self.play_button.set_sensitive(False)

    def play(self):
        """Update the play or pause picto on the gtk button.
        """
        TaskBase.play(self)
        if self.is_playing:
            img = 'pause'
        else:
            img = 'play'
        image = self.__get_image('%s_very_small' % img)
        if image:
            self.play_button.set_image(image)

    def set_title(self, text):
        """Simple title label update. Can be used at the end somewhere
        else to pass a message to the user.
        """
        if not self.__can_draw:
            return
        self.__can_draw = False
        self.__progression_title.set_markup('<b>%s</b>' % text)
        self.__can_draw = True

    def set_text(self, text):
        """Simple progress info label update. Can be used at the end somewhere
        else to pass a message to the user.
        """
        if not self.__can_draw:
            return
        self.__can_draw = False
        self.__progression_label.set_markup('<small>%s</small>' % text)
        self.__can_draw = True

    def set_sensitive(self, sensitive):
        """Active/deactive buttons, in case of non user manipulation
        expectation.
        """
        self.play_button.set_sensitive(sensitive)
        self.stop_button.set_sensitive(sensitive)
        self.remove_button.set_sensitive(sensitive)

    def __on_key_press(self, widget, event):
        """Catch the buttton enter press event.
        """
        if keyval_name(event.keyval) == 'Return':
            pass
        if keyval_name(event.keyval) == 'Escape':
            pass