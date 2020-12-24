# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CreateCardSetDialog.py
# Compiled at: 2019-12-11 16:37:48
"""Get details for a new card set"""
import gtk
from sqlobject import SQLObjectNotFound
from .SutekhDialog import SutekhDialog, do_complaint_error
from .CardSetsListView import CardSetsListView
from .AutoScrolledWindow import AutoScrolledWindow
from ..core.BaseTables import MAX_ID_LENGTH
from ..core.BaseAdapters import IPhysicalCardSet

def make_scrolled_text(oCardSet, sAttr):
    """Create a text buffer wrapped in a scrolled window, filled with
       the contents of sAtter if available"""
    oTextView = gtk.TextView()
    oBuffer = oTextView.get_buffer()
    oScrolledWin = AutoScrolledWindow(oTextView)
    if oCardSet:
        sValue = getattr(oCardSet, sAttr)
        if sValue:
            oBuffer.set_text(sValue)
    return (
     oBuffer, oScrolledWin)


class CreateCardSetDialog(SutekhDialog):
    """Prompt the user for the name of a new card set.

       Optionally, get Author + Description.
       """

    def __init__(self, oParent, sName=None, oCardSet=None, oCardSetParent=None):
        super(CreateCardSetDialog, self).__init__('Card Set Details', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_OK, gtk.RESPONSE_OK,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        oNameLabel = gtk.Label('Card Set Name : ')
        self.oName = gtk.Entry(MAX_ID_LENGTH)
        oAuthorLabel = gtk.Label('Author : ')
        self.oAuthor = gtk.Entry()
        oCommentriptionLabel = gtk.Label('Description : ')
        self.oCommentBuffer, oCommentWin = make_scrolled_text(oCardSet, 'comment')
        oParentLabel = gtk.Label('This card set is a subset of : ')
        self.oParentList = CardSetsListView(None, self)
        self.oParentList.set_size_request(100, 200)
        oAnnotateLabel = gtk.Label('Annotations : ')
        self.oAnnotateBuffer, oAnnotateWin = make_scrolled_text(oCardSet, 'annotations')
        self.oInUse = gtk.CheckButton('Mark card Set as In Use')
        self.set_default_size(500, 500)
        self.vbox.pack_start(oNameLabel, expand=False)
        self.vbox.pack_start(self.oName, expand=False)
        self.vbox.pack_start(oAuthorLabel, expand=False)
        self.vbox.pack_start(self.oAuthor, expand=False)
        self.vbox.pack_start(oCommentriptionLabel, expand=False)
        self.vbox.pack_start(oCommentWin, expand=True)
        self.vbox.pack_start(oParentLabel, expand=False)
        self.vbox.pack_start(AutoScrolledWindow(self.oParentList), expand=True)
        self.vbox.pack_start(oAnnotateLabel, expand=False)
        self.vbox.pack_start(oAnnotateWin, expand=True)
        self.vbox.pack_start(self.oInUse, expand=False)
        self.connect('response', self.button_response)
        self.show_all()
        self.sOrigName = sName
        if sName is not None:
            self.oName.set_text(sName)
        if oCardSet is not None:
            if not sName:
                self.oName.set_text(oCardSet.name)
                self.sOrigName = oCardSet.name
                self.oParentList.exclude_set(self.sOrigName)
            if oCardSetParent is None and oCardSet.parent is not None:
                self.oParentList.set_selected_card_set(oCardSet.parent.name)
            if oCardSet.author is not None:
                self.oAuthor.set_text(oCardSet.author)
            self.oInUse.set_active(oCardSet.inuse)
        self.sName = None
        self.sAuthor = None
        self.oParent = oCardSetParent
        return

    def get_name(self):
        """Get the name entered by the user"""
        return self.sName

    def get_author(self):
        """Get the author value"""
        return self.sAuthor

    def get_comment(self):
        """Get the comment value"""
        sComment = self.oCommentBuffer.get_text(self.oCommentBuffer.get_start_iter(), self.oCommentBuffer.get_end_iter())
        return sComment

    def get_annotations(self):
        """Get the comment value"""
        sAnnotations = self.oAnnotateBuffer.get_text(self.oAnnotateBuffer.get_start_iter(), self.oAnnotateBuffer.get_end_iter())
        return sAnnotations

    def get_parent(self):
        """Get the chosen parent card set, or None if 'No Parent' is chosen"""
        return self.oParent

    def get_in_use(self):
        """Get the In Use checkbox status"""
        return self.oInUse.get_active()

    def button_response(self, _oWidget, iResponse):
        """Handle button press from the dialog."""
        if iResponse == gtk.RESPONSE_OK:
            self.sName = self.oName.get_text()
            self.sAuthor = self.oAuthor.get_text()
            if self.sName:
                self.sName = self.sName.replace('<', '(')
                self.sName = self.sName.replace('>', ')')
                if self.sName != self.sOrigName:
                    try:
                        IPhysicalCardSet(self.sName)
                        do_complaint_error('Chosen Card Set Name is already in use')
                        self.sName = None
                        self.destroy()
                        return
                    except SQLObjectNotFound:
                        pass

                sParent = self.oParentList.get_selected_card_set()
                if sParent:
                    self.oParent = IPhysicalCardSet(sParent)
                else:
                    self.oParent = None
            else:
                self.sName = None
                do_complaint_error('You did not specify a name for the Card Set.')
        self.destroy()
        return