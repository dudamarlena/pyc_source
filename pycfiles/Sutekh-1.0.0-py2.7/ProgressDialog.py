# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/ProgressDialog.py
# Compiled at: 2019-12-11 16:37:48
"""classes needed for the progress dialog"""
import string
from logging import Handler
import gtk

class SutekhLogHandler(Handler, object):
    """Base class for loggers to talk to the dialog"""

    def __init__(self):
        super(SutekhLogHandler, self).__init__()
        self.oDialog = None
        return

    def set_dialog(self, oDialog):
        """point to the progress dialog"""
        self.oDialog = oDialog

    def emit(self, _oRecord):
        """Default emit handler"""
        pass


class SutekhHTMLLogHandler(SutekhLogHandler):
    """Logging class for cardlist and rulings parser.

       Converts messages of the form 'Card: X' into an approximate
       progress measure
       """

    def emit(self, oRecord):
        """Massage message into progress value.

           Skip difficult cases (The X, non-ascii characters, etc.)
           """
        if self.oDialog is None:
            return
        else:
            sString = oRecord.getMessage()
            if sString.startswith('Card: The '):
                return
            sBase = sString[6:8]
            sStart = string.upper(sBase)
            if sStart == sBase:
                return
            if sStart[0] not in string.ascii_uppercase or sStart[1] not in string.ascii_uppercase:
                return
            iPos = ord(sStart[0]) * 26 + ord(sStart[1]) - ord('A') * 27
            fBarPos = iPos / float(676)
            self.oDialog.update_bar(fBarPos)
            return


class SutekhCountLogHandler(SutekhLogHandler):
    """LogHandler class for dealing with database upgrade messages.

       Each message (Card List, card set, etc). is taken as a step in the
       process.
       """

    def __init__(self):
        super(SutekhCountLogHandler, self).__init__()
        self.iCount = None
        self.fTot = None
        return

    def set_total(self, iTot):
        """Set the total number of steps."""
        self.fTot = float(iTot)
        self.iCount = 0

    def emit(self, _oRecord):
        """Handle a emitted signal, updating the progress count."""
        if self.oDialog is None:
            return
        else:
            self.iCount += 1
            fBarPos = self.iCount / self.fTot
            self.oDialog.update_bar(fBarPos)
            return


class ProgressDialog(gtk.Window):
    """Show a window with a single progress bar."""

    def __init__(self):
        super(ProgressDialog, self).__init__()
        self.set_title('Progress')
        self.set_name('Sutekh.dialog')
        self.oProgressBar = gtk.ProgressBar()
        self.oProgressBar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
        self.oProgressBar.set_text('% done')
        self.oProgressBar.set_fraction(0.0)
        self.oProgressBar.set_size_request(350, 50)
        self.set_default_size(400, 100)
        self.oVBox = gtk.VBox()
        self.oDescription = gtk.Label('Unknown')
        self.oVBox.pack_start(self.oDescription)
        oAlign = gtk.Alignment(xalign=0.5, yalign=0.0)
        oAlign.add(self.oProgressBar)
        self.oVBox.pack_end(oAlign)
        self.add(self.oVBox)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        self.show_all()
        self.set_modal(True)

    def set_description(self, sDescription):
        """Change the description of a dialog"""
        self.oVBox.remove(self.oDescription)
        self.oDescription = gtk.Label(sDescription)
        self.oVBox.pack_start(self.oDescription)
        self.show_all()

    def reset(self):
        """Reset the progress bar to zero"""
        self.update_bar(0.0)

    def set_complete(self):
        """Set the progress bar as being complete."""
        self.update_bar(1.0)

    def update_bar(self, fStep):
        """Update the progress bar to the given fStep value."""
        if fStep > 1.0:
            self.oProgressBar.set_fraction(1.0)
            self.oProgressBar.set_text('100% complete')
        else:
            if fStep < 0.0:
                self.oProgressBar.set_fraction(0.0)
                self.oProgressBar.set_text(' 0% complete')
            else:
                self.oProgressBar.set_fraction(fStep)
                self.oProgressBar.set_text('%2.0f%% complete' % (fStep * 100))
            while gtk.events_pending():
                gtk.main_iteration()