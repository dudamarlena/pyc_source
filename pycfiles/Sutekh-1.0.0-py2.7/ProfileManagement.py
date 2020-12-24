# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/ProfileManagement.py
# Compiled at: 2019-12-11 16:37:48
"""Allow the user to delete / edit the various profiles"""
import gtk, gobject
from sqlobject import SQLObjectNotFound
from ..core.BaseTables import PhysicalCardSet
from .SutekhDialog import NotebookDialog, do_complaint_error, do_complaint_warning
from .AutoScrolledWindow import AutoScrolledWindow
from .FrameProfileEditor import FrameProfileEditor
from .BaseConfigFile import CARDSET, FULL_CARDLIST, CARDSET_LIST
LABELS = {CARDSET: 'Card Set Profiles', 
   FULL_CARDLIST: 'Full Cardlist Profiles', 
   CARDSET_LIST: 'Card Set List Profiles'}

class ProfileListStore(gtk.ListStore):
    """Simple list store for profiles widget"""

    def __init__(self):
        super(ProfileListStore, self).__init__(gobject.TYPE_STRING, gobject.TYPE_STRING)

    def fill_list(self, aVals):
        """Fill the list"""
        self.clear()
        for tEntry in aVals:
            self.append(row=tEntry)

    def _find_iter(self, sProfile):
        """Find the correct iter for an entry"""
        oIter = self.get_iter_root()
        while oIter:
            if sProfile == self.get_value(oIter, 0):
                return oIter
            oIter = self.iter_next(oIter)

        return

    def fix_entry(self, sProfile, sNewName):
        """Fix the value for the given profile"""
        oIter = self._find_iter(sProfile)
        if oIter:
            self.set_value(oIter, 1, sNewName)

    def remove_entry(self, sProfile):
        """Fix the value for the given profile"""
        oIter = self._find_iter(sProfile)
        if oIter:
            self.remove(oIter)


class ProfileListView(gtk.TreeView):
    """Simple tree view for the profile list"""

    def __init__(self, sTitle):
        oModel = ProfileListStore()
        super(ProfileListView, self).__init__(oModel)
        oCell1 = gtk.CellRendererText()
        oColumn1 = gtk.TreeViewColumn(sTitle, oCell1, text=1)
        self.append_column(oColumn1)
        self.get_selection().set_mode(gtk.SELECTION_SINGLE)

    def get_selected(self):
        """Get the of selected value"""
        oModel, aSelectedRows = self.get_selection().get_selected_rows()
        for oPath in aSelectedRows:
            oIter = oModel.get_iter(oPath)
            sProfile = oModel.get_value(oIter, 0)
            sName = oModel.get_value(oIter, 1)
            return (sProfile, sName)

        return


class ScrolledProfileList(gtk.Frame):
    """Frame containing the scrolled list of profiles"""

    def __init__(self, sTitle):
        super(ScrolledProfileList, self).__init__(None)
        self._oView = ProfileListView(sTitle)
        self._oStore = self._oView.get_model()
        oMyScroll = AutoScrolledWindow(self._oView)
        self.add(oMyScroll)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.show_all()
        return

    store = property(fget=lambda self: self._oStore, doc='List of values')
    view = property(fget=lambda self: self._oView, doc='List of values')


class ProfileMngDlg(NotebookDialog):
    """Dialog which allows the user to delete and edit profiles."""
    RESPONSE_EDIT = 1
    RESPONSE_DELETE = 2

    def __init__(self, oParent, oConfig):
        super(ProfileMngDlg, self).__init__('Manage Profiles', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.__oParent = oParent
        self.__oConfig = oConfig
        self._dLists = {}
        self.set_default_size(700, 550)
        for sType in (CARDSET, FULL_CARDLIST, CARDSET_LIST):
            oProfileList = self._make_profile_list(sType)
            self.add_widget_page(oProfileList, LABELS[sType])
            self._dLists[oProfileList] = sType

        self.action_area.pack_start(gtk.VSeparator(), expand=True)
        self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        self.add_first_button('Delete', self.RESPONSE_DELETE)
        self.add_first_button('Edit Profile', self.RESPONSE_EDIT)
        self.connect('response', self._button_response)
        self.show_all()

    def _make_profile_list(self, sType):
        """Create a list of the available profiles"""
        oList = ScrolledProfileList(LABELS[sType])
        aProfiles = set(self.__oConfig.profiles(sType))
        aNames = [('defaults', 'Default')]
        for sProfile in list(sorted(aProfiles)):
            sName = self.__oConfig.get_profile_option(sType, sProfile, 'name')
            aNames.append((sProfile, sName))

        oList.store.fill_list(aNames)
        return oList

    def _button_response(self, _oWidget, iResponse):
        """Handle the button choices from the user.

           If the operation doesn't close the dialog we rerun the main
           dialog loop, waiting for another user button press (same
           logic as FilterDialog).
           """
        if iResponse == self.RESPONSE_EDIT:
            self._edit_profile()
            return self.run()
        if iResponse == self.RESPONSE_DELETE:
            self._delete_profile()
            return self.run()
        return iResponse

    def _get_selected_profile(self):
        """Get the currently selected profile and type"""
        oList = self.get_cur_widget()
        sType = self._dLists[oList]
        tSelected = oList.view.get_selected()
        if tSelected:
            sProfile, sName = tSelected
        else:
            sProfile, sName = (None, None)
        return (
         sType, sProfile, sName)

    def _edit_profile(self):
        """Fire off the profile editor"""
        sType, sProfile, sName = self._get_selected_profile()
        if sProfile:
            sOldName = sName
            oEditDlg = FrameProfileEditor(self.__oParent, self.__oConfig, sType)
            oEditDlg.set_selected_profile(sProfile)
            oEditDlg.run()
            sNewName = self.__oConfig.get_profile_option(sType, sProfile, 'name')
            if sNewName != sOldName:
                oList = self.get_cur_widget()
                oList.store.fix_entry(sProfile, sNewName)

    def _get_in_use_mesg(self, sType, aPanes):
        """Return a suitable 'profile in use' message for profile deletion"""
        if sType in (CARDSET_LIST, FULL_CARDLIST):
            return 'Profile is in use. Really delete?'
        else:
            aOpenPanes = []
            aClosedPanes = []
            for sId in aPanes:
                if sId.startswith('cs'):
                    iCSid = int(sId[2:])
                    try:
                        oCS = PhysicalCardSet.get(iCSid)
                    except SQLObjectNotFound:
                        self.__oConfig.clear_cardset_profile(sId)
                        continue

                    aCSPanes = self.__oParent.find_cs_pane_by_set_name(oCS.name)
                    if aCSPanes:
                        for oPane in aCSPanes:
                            aOpenPanes.append(oPane.title)

                    else:
                        aClosedPanes.append(oCS.name)
                else:
                    iPaneId = int(sId[4:])
                    oCSFrame = self.__oParent.find_pane_by_id(iPaneId)
                    aOpenPanes.append(oCSFrame.title)

            sMesg = 'This profile is in use. Really delete?\n'
            if aOpenPanes:
                sMesg += '\nThe following open panes reference this  profile\n' + ('\n').join(aOpenPanes)
            if aClosedPanes:
                sMesg += '\nThe following card closed card sets reference this profile\n' + ('\n').join(aClosedPanes)
            return sMesg

    def _delete_profile(self):
        """Delete the given profile"""
        sType, sProfile, _sName = self._get_selected_profile()
        if sProfile:
            if sProfile == 'defaults':
                do_complaint_error("You can't delete the default profile")
                return
            aPanes = self.__oConfig.get_profile_users(sType, sProfile)
            if aPanes:
                sMesg = self._get_in_use_mesg(sType, aPanes)
                iRes = do_complaint_warning(sMesg)
                if iRes == gtk.RESPONSE_CANCEL:
                    return
            self.__oConfig.remove_profile(sType, sProfile)
            oList = self.get_cur_widget()
            oList.store.remove_entry(sProfile)