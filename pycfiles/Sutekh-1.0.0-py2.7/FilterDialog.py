# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/FilterDialog.py
# Compiled at: 2019-12-11 16:37:48
"""Allow the user to specify a filter."""
import gtk, gobject
from ..core import FilterParser
from .SutekhDialog import SutekhDialog, do_complaint_error, do_complaint_buttons
from .BaseConfigFile import FULL_CARDLIST, CARDSET, DEF_PROFILE_FILTER
from .MessageBus import MessageBus, CONFIG_MSG
from .FilterEditor import FilterEditor

class FilterDialog(SutekhDialog):
    """Dialog which allows the user to select and edit filters.

       This dialog exists per card list view, and keeps state during
       a session by never being destoryed - just hiding itself when
       needed.

       This also listens to Config File events, so the list of available
       filters remains syncronised across the different views.
       """
    RESPONSE_CLEAR = 1
    RESPONSE_REVERT = 2
    RESPONSE_LOAD = 3
    RESPONSE_SAVE = 4
    RESPONSE_DELETE = 5
    INITIAL_FILTER = 'Default Filter Template'

    def __init__(self, oParent, oConfig, sFilterType, sDefaultFilter=None):
        super(FilterDialog, self).__init__('Specify Filter', oParent, gtk.DIALOG_DESTROY_WITH_PARENT)
        self._oAccelGroup = gtk.AccelGroup()
        self.__oParent = oParent
        self.__bWasCancelled = False
        self.__oParser = FilterParser.FilterParser()
        self.__oConfig = oConfig
        self.__sFilterType = sFilterType
        self.__oFilter = None
        self.__oFilterEditor = FilterEditor(None, self.__sFilterType, self.__oParser, self)
        self.__oFilterEditor.connect_name_changed(self.__name_changed)
        self.__sOriginalName = None
        self.__sOriginalAST = None
        self.set_default_size(700, 550)
        self.connect('response', self.__button_response)
        self._aDefaultFilters = oConfig.get_default_filters()
        self.add_button('Clear Filter', self.RESPONSE_CLEAR)
        self.add_button('Revert Filter', self.RESPONSE_REVERT)
        self.add_button('Load', self.RESPONSE_LOAD)
        self.add_button('Save', self.RESPONSE_SAVE)
        self.add_button('Delete', self.RESPONSE_DELETE)
        self.action_area.pack_start(gtk.VSeparator(), expand=True)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.vbox.pack_start(self.__oFilterEditor)
        aDefaultFilters = self.__fetch_filters(True)
        aConfigFilters = self.__fetch_filters(False)
        if sDefaultFilter:
            try:
                oAST = self.__oParser.apply(sDefaultFilter)
            except Exception:
                sDefaultFilter = None

        if sDefaultFilter:
            sName, sFilter = '', sDefaultFilter
            oAST = self.__oParser.apply(sFilter)
        elif aDefaultFilters:
            sName, sFilter = aDefaultFilters[0]
            oAST = self.__oParser.apply(sFilter)
        elif aConfigFilters:
            sName, sFilter = aConfigFilters[0]
            oAST = self.__oParser.apply(sFilter)
        else:
            sName, oAST = ('', None)
        self.__load_filter(sName, oAST)
        self.add_accel_group(self._oAccelGroup)
        MessageBus.subscribe(CONFIG_MSG, 'replace_filter', self.replace_filter)
        MessageBus.subscribe(CONFIG_MSG, 'add_filter', self.add_filter)
        MessageBus.subscribe(CONFIG_MSG, 'remove_filter', self.remove_filter)
        self.show_all()
        return

    accel_group = property(fget=lambda self: self._oAccelGroup, doc='Dialog Accelerator group')

    def __button_response(self, _oWidget, iResponse):
        """Handle the button choices from the user.

           If the operation doesn't close the dialog, such as the
           filter manipulation options, we short circuit the signal
           handling, and prevent anything propogating to the
           window waiting for the dialog.
           """
        if iResponse == gtk.RESPONSE_OK:
            self.__bWasCancelled = False
            self.__oFilter = self.__oFilterEditor.get_filter()
        else:
            if iResponse == self.RESPONSE_CLEAR:
                self.__clear_filter()
                return True
            if iResponse == self.RESPONSE_REVERT:
                self.__revert_filter()
                return True
            if iResponse == self.RESPONSE_LOAD:
                self.__run_load_dialog()
                return True
            if iResponse == self.RESPONSE_SAVE:
                self.__save_filter()
                return True
            if iResponse == self.RESPONSE_DELETE:
                self.__delete_filter()
                return True
            self.__bWasCancelled = True
        self.hide()
        return False

    def __run_load_dialog(self):
        """Display a dialog for loading a filter."""
        oLoadDialog = SutekhDialog('Load Filter', self.__oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        oLoadDialog.set_keep_above(True)
        oLoadDialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        oLoadDialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        oFilterStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_STRING)

        def iter_to_text(_oLayout, oCell, oModel, oIter):
            """Convert the model entry at oIter into the correct text"""
            bDefault = oModel.get_value(oIter, 0)
            sName = oModel.get_value(oIter, 1)
            if bDefault:
                oCell.set_property('text', sName + ' (built-in)')
            else:
                oCell.set_property('text', sName)

        for bDefault in (True, False):
            for sName, sFilter in self.__fetch_filters(bDefault):
                oIter = oFilterStore.append(None)
                oFilterStore.set(oIter, 0, bDefault, 1, sName, 2, sFilter)

        oFilterSelector = gtk.ComboBox(oFilterStore)
        oCell = gtk.CellRendererText()
        oFilterSelector.pack_start(oCell, True)
        oFilterSelector.set_cell_data_func(oCell, iter_to_text)
        oLoadDialog.vbox.pack_start(oFilterSelector)
        oLoadDialog.show_all()
        try:
            iResponse = oLoadDialog.run()
            oIter = oFilterSelector.get_active_iter()
            if iResponse == gtk.RESPONSE_OK and oIter:
                sName = oFilterStore.get_value(oIter, 1)
                sFilter = oFilterStore.get_value(oIter, 2)
                oAST = self.__oParser.apply(sFilter)
                self.__load_filter(sName, oAST)
        finally:
            oLoadDialog.destroy()

        return

    def __fetch_filters(self, bDefault):
        """Load filters from config or default list.

           Returns a (sName, sFilter) list.
           """
        if bDefault:
            sSrc = 'default filter list'
            oFilterIter = list(self._aDefaultFilters.items())
        else:
            sSrc = 'config file'
            oFilterIter = list(self.__oConfig.get_filter_keys())
        aFilters = []
        aErrMsgs = []
        for sName, sFilter in oFilterIter:
            try:
                oAST = self.__oParser.apply(sFilter)
                if sName.lower() == DEF_PROFILE_FILTER.lower():
                    raise RuntimeError('Reserved name used for filter name')
                if oAST.get_filter_expression() is None or self.__sFilterType in oAST.get_type():
                    aFilters.append((sName, sFilter))
            except Exception:
                aErrMsgs.append("%s (filter: '%s')" % (sName, sFilter))
                if not bDefault:
                    self.__oConfig.remove_filter(sFilter, sName)
                else:
                    del self._aDefaultFilters[sName]

        if aErrMsgs:
            do_complaint_error('The following invalid filters have been removed from the %s:\n' % (
             sSrc,) + ('\n').join(aErrMsgs))

        def filter_key(tFiltInfo):
            """We sort filters alphabetically by name, but with default
               filter first if it is present"""
            if tFiltInfo[0] == self.INITIAL_FILTER:
                return ''
            return tFiltInfo[0]

        aFilters.sort(key=filter_key)
        return aFilters

    def __load_filter(self, sName, oAST):
        """Set the current filter to sName, oAST."""
        self.__sOriginalName = sName
        self.__sOriginalAST = oAST
        self.__oFilterEditor.set_name(sName)
        self.__oFilterEditor.replace_ast(oAST)
        self.__update_sensitivity()

    def __revert_filter(self):
        """Revert the filter to the last one set."""
        self.__oFilterEditor.set_name(self.__sOriginalName)
        self.__oFilterEditor.replace_ast(self.__sOriginalAST)
        self.__update_sensitivity()

    def __clear_filter(self):
        """Clear the filter AST."""
        self.__oFilterEditor.set_name('')
        self.__oFilterEditor.replace_ast(None)
        self.__update_sensitivity()
        return

    def __save_filter(self):
        """Save the filter to the config."""
        sName = self.__oFilterEditor.get_name()
        sFilter = self.__oFilterEditor.get_current_text()
        sConfigFilter = self.__oConfig.get_filter(sName)
        bSaved = False
        if sName.lower() == DEF_PROFILE_FILTER.lower():
            do_complaint_error('%s is a reserved filter name.\nNot Saving' % sName)
            return
        else:
            if sConfigFilter is not None:
                iResponse = do_complaint_buttons("Replace existing filter '%s'?" % (sName,), gtk.MESSAGE_QUESTION, (
                 gtk.STOCK_YES, gtk.RESPONSE_YES,
                 gtk.STOCK_NO, gtk.RESPONSE_NO))
                if iResponse == gtk.RESPONSE_YES:
                    self.__oConfig.replace_filter(sName, sConfigFilter, sFilter)
                    bSaved = True
            else:
                self.__oConfig.add_filter(sName, sFilter)
                bSaved = True
            if bSaved:
                self.__oConfig.update_filter_list()
                oAST = self.__oParser.apply(sFilter)
                self.__load_filter(sName, oAST)
            return

    def __delete_filter(self):
        """Delete the filter from the config."""
        sName = self.__oFilterEditor.get_name()
        sConfigFilter = self.__oConfig.get_filter(sName)
        dProfiles = self.__oConfig.get_profiles_for_filter(sName)
        if sConfigFilter is not None:
            if dProfiles[FULL_CARDLIST] or dProfiles[CARDSET]:
                sCardlist = ('\n').join([ 'Cardlist profile : %s' % self.__oConfig.get_profile_option(FULL_CARDLIST, x, 'name') for x in dProfiles[FULL_CARDLIST]
                                        ])
                sCardset = ('\n').join([ 'Cardset profile : %s' % self.__oConfig.get_profile_option(CARDSET, x, 'name') for x in dProfiles[CARDSET]
                                       ])
                sProfiles = ('\n').join([sCardlist, sCardset])
                iResponse = do_complaint_buttons("Filter '%s' used in the followin profiles:\n%s\nReally delete?" % (
                 sName, sProfiles), gtk.MESSAGE_QUESTION, (gtk.STOCK_YES, gtk.RESPONSE_YES,
                 gtk.STOCK_NO, gtk.RESPONSE_NO))
                if iResponse == gtk.RESPONSE_YES:
                    self.__oConfig.remove_filter(sName, sConfigFilter)
                else:
                    return
            else:
                self.__oConfig.remove_filter(sName, sConfigFilter)
        self.__load_filter('', None)
        self.__oConfig.update_filter_list()
        return

    def __update_sensitivity(self):
        """Update which responses are available."""
        sName = self.__oFilterEditor.get_name()
        sConfigFilter = self.__oConfig.get_filter(sName)
        if sName:
            self.set_response_sensitive(self.RESPONSE_SAVE, True)
        else:
            self.set_response_sensitive(self.RESPONSE_SAVE, False)
        if sName == self.__sOriginalName and sConfigFilter is not None:
            self.set_response_sensitive(self.RESPONSE_DELETE, True)
        else:
            self.set_response_sensitive(self.RESPONSE_DELETE, False)
        return

    def __name_changed(self, _oNameEntry):
        """Callback for connecting to filter editor name change events."""
        self.__update_sensitivity()

    def get_filter(self):
        """Get the current filter for this dialog."""
        return self.__oFilter

    def was_cancelled(self):
        """Return true if the user cancelled the filter dialog."""
        return self.__bWasCancelled

    def replace_filter(self, _sId, _sOldFilter, _sNewFilter):
        """Handle a filter in the config file being replaced."""
        self.__update_sensitivity()

    def add_filter(self, _sId, _sFilter):
        """Handle filter being added to the config file."""
        self.__update_sensitivity()

    def remove_filter(self, _sId, _sFilter):
        """Handle a filter being removed from the config file."""
        self.__update_sensitivity()