# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/widgets/threaded_task_box.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3875 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from mvc.support.cancellable_thread import CancellableThread
from mvc.support.gui_loop import add_timeout_call, remove_timeout_call, run_when_idle

class ThreadedTaskBox(Gtk.Table):
    __doc__ = '\n        ThreadedTaskBox: encapsulates a spinner, label and a cancel button for\n        threaded tasks.\n    '
    __gsignals__ = {'cancelrequested':(
      GObject.SignalFlags.RUN_LAST, None, (GObject.TYPE_PYOBJECT,)), 
     'stoprequested':(
      GObject.SignalFlags.RUN_LAST, None, (GObject.TYPE_PYOBJECT,))}

    def __init__(self, cancelable=True, stoppable=False):
        """
            Create a ThreadedTaskBox

            Keyword arguments:
            cancelable -- optional value to determine whether to show cancel button. Defaults to True.
            stoppable -- optional value to determine whether to show the stop button. Default to False.
        """
        super(ThreadedTaskBox, self).__init__()
        self.setup_ui(cancelable=cancelable, stoppable=stoppable)

    def setup_ui(self, cancelable=True, stoppable=False):
        GObject.GObject.__init__(self, 3, 3)
        self.set_row_spacings(10)
        self.set_col_spacings(10)
        self.descrlbl = Gtk.Label(label='Status:')
        self.descrlbl.show()
        self.attach((self.descrlbl), 0, 3, 0, 1, xoptions=(Gtk.AttachOptions.FILL), yoptions=0)
        self.spinner = Gtk.Spinner()
        self.spinner.show()
        self.attach((self.spinner), 0, 1, 1, 3, xoptions=0, yoptions=0)
        self.label = Gtk.Label()
        self.label.show()
        self.attach((self.label), 1, 2, 1, 3, xoptions=(Gtk.AttachOptions.FILL), yoptions=0)
        self.cancel_button = Gtk.Button(stock=(Gtk.STOCK_CANCEL))
        self.cancel_button.set_sensitive(False)
        self.cancel_button.connect('clicked', self._ThreadedTaskBox__cancel_clicked)
        if cancelable:
            self.attach((self.cancel_button), 2, 3, 1, 2, xoptions=0, yoptions=0)
        self.stop_button = Gtk.Button(stock=(Gtk.STOCK_STOP))
        self.stop_button.set_sensitive(False)
        self.stop_button.connect('clicked', self._ThreadedTaskBox__stop_clicked)
        if stoppable:
            self.attach((self.stop_button), 2, 3, 2, 3, xoptions=0, yoptions=0)
        self.set_no_show_all(False)
        self.set_visible(True)
        self.show_all()

    def start(self):
        self.spinner.start()
        self.cancel_button.set_sensitive(True)
        self.stop_button.set_sensitive(True)

    def set_status(self, caption):
        self.label.set_text(caption)

    def stop(self, join=False, cancel=False):
        """
            Stops spinning the spinner and emits the correct event.
        """
        self.cancel_button.set_sensitive(False)
        self.stop_button.set_sensitive(False)
        if cancel:
            self.emit('cancelrequested', self)
        else:
            self.emit('stoprequested', self)
        self.spinner.stop()
        self.label.set_text('Done')

    def cancel(self):
        self.stop(cancel=True)

    def __cancel_clicked(self, widget):
        self.cancel()

    def __stop_clicked(self, widget):
        self.stop()


GObject.type_register(ThreadedTaskBox)