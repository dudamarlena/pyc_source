# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/SutekhDialog.py
# Compiled at: 2019-12-11 16:37:48
"""Dialog wrapper and functions for Sutekh"""
import logging, sys, traceback, gtk
from gobject import markup_escape_text
from sutekh.SutekhInfo import SutekhInfo as AppInfo
from ..Utility import get_database_url

class SutekhDialog(gtk.Dialog):
    """wrapper class for gtk.Dialog"""

    def __init__(self, sTitle, oParent=None, iFlags=0, oButtons=None):
        super(SutekhDialog, self).__init__(sTitle, oParent, iFlags, oButtons)
        self.set_name('Sutekh.dialog')

    def add_first_button(self, sText, iResponse):
        """Abuse add_button and action_area to insert a button at the
           head of the list."""
        oButton = self.add_button(sText, iResponse)
        self.action_area.reorder_child(oButton, 0)


def do_complaint(sMessage, oDialogType, oButtonType, bMarkup=False):
    """Wrapper function for gtk.MessageDialog.

       Create the dialog, run it, and return the result. If bMarkup is true,
       the string is interpreted as markup, other, just as plain text
       """
    if bMarkup:
        oComplaint = gtk.MessageDialog(None, 0, oDialogType, oButtonType, None)
        oComplaint.set_markup(sMessage)
    else:
        oComplaint = gtk.MessageDialog(None, 0, oDialogType, oButtonType, sMessage)
    oComplaint.set_name('Sutekh.dialog')
    iResponse = oComplaint.run()
    oComplaint.destroy()
    return iResponse


def do_complaint_buttons(sMessage, oType, aButtonInfo, bMarkup=False):
    """Wrapper function for gtk.MessageDialog, using add_button to create
       custom button layouts.

       Create the dialog, run it, and return the result. If bMarkup is true,
       the string is interpreted as markup, other, just as plain text.
       """
    if bMarkup:
        oComplaint = gtk.MessageDialog(None, 0, oType, gtk.BUTTONS_NONE, None)
        oComplaint.set_markup(sMessage)
    else:
        oComplaint = gtk.MessageDialog(None, 0, oType, gtk.BUTTONS_NONE, sMessage)
    for oItem, oResponse in zip(aButtonInfo[0::2], aButtonInfo[1::2]):
        oComplaint.add_button(oItem, oResponse)

    oComplaint.set_name('Sutekh.dialog')
    iResponse = oComplaint.run()
    oComplaint.destroy()
    return iResponse


def do_complaint_error(sMessage):
    """Error dialog with close button"""
    return do_complaint(sMessage, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, False)


def do_complaint_warning(sMessage):
    """Warning dialog with OK and CANCEL buttons"""
    return do_complaint(sMessage, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL, False)


class DetailDialog(SutekhDialog):
    """Message dialog with a details expander"""

    def __init__(self, sMessage, sDetails):
        super(DetailDialog, self).__init__('%s has encounterd an error' % AppInfo.NAME, oButtons=(
         gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        oHBox = gtk.HBox(False, 2)
        oMessageBox = gtk.VBox(False, 2)
        oImage = gtk.Image()
        oImage.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
        oImage.set_alignment(0, 0)
        oHBox.pack_start(oImage, expand=False)
        oInfo = gtk.Label()
        oInfo.set_markup('<b>%s</b>' % markup_escape_text(sMessage))
        oInfo.set_alignment(0, 0)
        oInfo.set_selectable(True)
        oMessageBox.pack_start(oInfo, expand=False)
        oExpander = gtk.Expander('Details')
        oFrame = gtk.Frame()
        oDetails = gtk.Label(sDetails)
        oDetails.set_selectable(True)
        oFrame.add(oDetails)
        oExpander.add(oFrame)
        oMessageBox.pack_start(oExpander)
        oHBox.pack_start(oMessageBox)
        self.vbox.pack_start(oHBox)
        oExpander.set_expanded(False)
        self.show_all()
        self.set_name('Sutekh.dialog')


def format_app_info():
    """Format the application details nicely for the error dialogs."""
    return '%s version %s\nDatabase: %s\n\n' % (AppInfo.NAME,
     AppInfo.VERSION_STR,
     get_database_url())


def do_complaint_error_details(sMessage, sDetails):
    """Popup an details dialog for an error"""
    oComplaint = DetailDialog(sMessage, ('\n').join([format_app_info(),
     sDetails]))
    iResponse = oComplaint.run()
    oComplaint.destroy()
    return iResponse


def do_exception_complaint(sMessage):
    """Handle an exception - log the details for verbose info, and popup
       a detailed dialog with the info."""
    oType, oValue, oTraceback = sys.exc_info()
    aTraceback = traceback.format_exception(oType, oValue, oTraceback, limit=30)
    logging.error('%s:\n%s', sMessage, ('').join(aTraceback))
    do_complaint_error_details(sMessage, ('').join(aTraceback))


def exception_handler(oType, oValue, oTraceback):
    """sys.excepthook wrapper around do_complaint_error_details."""
    if oType == KeyboardInterrupt:
        return
    sMessage = '%s reported an unhandled exception:\n%s\n' % (AppInfo.NAME,
     str(oValue))
    aTraceback = traceback.format_exception(oType, oValue, oTraceback)
    sDetails = ('').join(aTraceback)
    logging.error('%s:\n%s', sMessage, ('\n').join([format_app_info(),
     sDetails]))
    do_complaint_error_details(sMessage, sDetails)


class NotebookDialog(SutekhDialog):
    """Dialog with a notebook widget."""

    def __init__(self, sTitle, oParent=None, iFlags=0, oButtons=None):
        super(NotebookDialog, self).__init__(sTitle, oParent, iFlags, oButtons)
        self._oNotebook = gtk.Notebook()
        self._oNotebook.set_scrollable(True)
        self._oNotebook.popup_enable()
        self.vbox.pack_start(self._oNotebook)

    notebook = property(fget=lambda self: self._oNotebook, doc='Notebook Widget')

    def add_widget_page(self, oWidget, sTabText, sMenuText=None, bMarkup=False):
        """Add a widget to the notebook as a page, specifying tab header.

           sMenuText can be used to control the text of the popup menu
           item.
           If bMarkup is True, the header text is interpreted as a markup
           string."""
        oHeader = gtk.Label()
        if bMarkup:
            oHeader.set_markup(sTabText)
        else:
            oHeader.set_text(sTabText)
        if sMenuText:
            oMenuLabel = gtk.Label(sMenuText)
            oMenuLabel.set_alignment(0.0, 0.5)
            self._oNotebook.append_page_menu(oWidget, oHeader, oMenuLabel)
        else:
            self._oNotebook.append_page(oWidget, oHeader)

    def get_cur_widget(self):
        """Get the main widget of the current page."""
        iPage = self._oNotebook.get_current_page()
        return self._oNotebook.get_nth_page(iPage)

    def iter_all_page_widgets(self):
        """Iterator over all the pages in the notebook, returning
           the main widget of each page."""
        for iPage in range(self._oNotebook.get_n_pages()):
            yield self._oNotebook.get_nth_page(iPage)