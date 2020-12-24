# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BasePluginManager.py
# Compiled at: 2019-12-11 16:37:48
"""Base Classes for managing and creating plugins for Sutekh
   derived card set managers."""
import os, glob, logging, re, zipfile, zipimport, gtk
from gobject import markup_escape_text
from sqlobject import sqlhub
from ..core.DatabaseVersion import DatabaseVersion
from ..core.BaseTables import PhysicalCardSet, PhysicalCard
from ..core.BaseAdapters import IAbstractCard
from .BaseConfigFile import CARDSET, FULL_CARDLIST, CARDSET_LIST, FRAME
from .MessageBus import MessageBus, CONFIG_MSG, DATABASE_MSG
from .SutekhDialog import do_complaint_warning

def submodules(oPackage):
    """List all the submodules in a package."""
    oLoader = getattr(oPackage, '__loader__', None)
    aModules = set()
    if isinstance(oLoader, zipimport.zipimporter):
        oPackageZip = zipfile.ZipFile(oLoader.archive)
        sPrefix = ('/').join(oPackage.__name__.split('.')) + '/'
        oModRe = re.compile('(?P<mod>[^/]*)\\.py[^/]*')
        for sFile in oPackageZip.namelist():
            if sFile.startswith(sPrefix):
                sFile = sFile[len(sPrefix):]
                oMatch = oModRe.match(sFile)
                if oMatch and oMatch.group('mod') != '__init__':
                    aModules.add(oMatch.group('mod'))

    else:
        sPackageDir = os.path.dirname(oPackage.__file__)
        for sModuleFile in glob.glob(os.path.join(sPackageDir, '*.py*')):
            sModule = os.path.basename(sModuleFile)
            sModule = os.path.splitext(sModule)[0]
            if sModule != '__init__':
                aModules.add(sModule)

    return list(aModules)


class BasePluginManager(object):
    """Base class for managing plugins.

       Plugin modules should be placed in the plugins package directory and
       contain an attribute named 'plugin' which points to the plugin class the
       module contains.
       """
    cAppPlugin = None
    sPluginDir = ''

    def __init__(self):
        self._aPlugins = []

    def _do_load_plugins(self, aPlugins):
        """Load list of Plugin Classes from plugin dir."""
        for sPluginName in submodules(aPlugins):
            try:
                mPlugin = __import__('%s.%s' % (self.sPluginDir, sPluginName), None, None, [aPlugins])
            except ImportError as oExp:
                logging.warn('Failed to load plugin %s (%s).', sPluginName, oExp, exc_info=1)
                continue

            try:
                cPlugin = mPlugin.plugin
            except AttributeError as oExp:
                logging.warn('Plugin module %s appears not to contain a plugin (%s).', sPluginName, oExp, exc_info=1)
                continue

            if issubclass(cPlugin, self.cAppPlugin):
                if hasattr(sqlhub, 'processConnection') and not cPlugin.check_versions():
                    continue
                self._aPlugins.append(cPlugin)

        return

    def load_plugins(self):
        """Entry point to load the plugins"""
        raise NotImplementedError

    def get_all_plugins(self):
        """Get all the plugins loaded"""
        return list(self._aPlugins)

    def get_plugins_for(self, cModelType):
        """Get the list of plugins which support the given model type."""
        return [ cPlugin for cPlugin in self._aPlugins if cPlugin.check_model_type(cModelType)
               ]


class PluginConfigFileListener(object):
    """Listen for messages and inform plugins when their config changes."""

    def __init__(self, oPlugin):
        self._oPlugin = oPlugin
        MessageBus.subscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)
        MessageBus.subscribe(CONFIG_MSG, 'profile_changed', self.profile_changed)

    def cleanup(self):
        """Unhook from the message bus"""
        MessageBus.unsubscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)
        MessageBus.unsubscribe(CONFIG_MSG, 'profile_changed', self.profile_changed)

    def profile_option_changed(self, sType, sProfile, sKey):
        """One of the per-deck configuration items changed."""
        if sType == CARDSET or sType == FRAME:
            dConfig = self._oPlugin.dPerPaneConfig
        elif sType == FULL_CARDLIST:
            dConfig = self._oPlugin.dCardListConfig
        elif sType == CARDSET_LIST:
            dConfig = self._oPlugin.dCardSetListConfig
        else:
            dConfig = {}
        if sKey in dConfig:
            oConfig = self._oPlugin.config
            if sType == CARDSET or sType == FRAME:
                tProfiles = (
                 oConfig.get_profile(FRAME, self._oPlugin.model.frame_id),
                 oConfig.get_profile(CARDSET, self._oPlugin.model.cardset_id))
            else:
                tProfiles = (oConfig.get_profile(sType, self._oPlugin.model.cardset_id),)
            if sProfile in tProfiles:
                self._oPlugin.perpane_config_updated()

    def profile_changed(self, sType, sId):
        """The profile associated with a frame changed."""
        if sType == FRAME and self._oPlugin.model.frame_id == sId:
            self._oPlugin.perpane_config_updated()
        elif sType in (CARDSET, FULL_CARDLIST, CARDSET_LIST) and self._oPlugin.model.cardset_id == sId:
            self._oPlugin.perpane_config_updated()


class BasePlugin(object):
    """Base class for plugins.

       Applications to derive their own subclass of this for their plugins."""
    dTableVersions = {}
    aModelsSupported = ()
    dGlobalConfig = {}
    dPerPaneConfig = {}
    dCardListConfig = {}
    dCardSetListConfig = {}

    def __init__(self, oCardListView, oCardListModel, cModelType=None):
        """oCardListModel - card list model for this plugin to operate on."""
        self._oView = oCardListView
        self._oModel = oCardListModel
        self._cModelType = cModelType
        self._oListener = None
        if self._oModel is not None and hasattr(self._oModel, 'frame_id'):
            self._oListener = PluginConfigFileListener(self)
        MessageBus.subscribe(DATABASE_MSG, 'update_to_new_db', self.update_to_new_db)
        MessageBus.subscribe(DATABASE_MSG, 'prepare_for_db_update', self.prepare_for_db_update)
        return

    parent = property(fget=lambda self: self._oView.mainwindow, doc='Parent window to use when creating dialogs.')
    view = property(fget=lambda self: self._oView, doc='Associated CardListView object.')
    model = property(fget=lambda self: self._oModel, doc='Associated CardModel object.')
    cardlookup = property(fget=lambda self: self.parent.cardLookup, doc='GUI CardLookup.')
    icon_manager = property(fget=lambda self: self.parent.icon_manager, doc='Icon manager.')
    config = property(fget=lambda self: self._oView.mainwindow.config_file, doc='Configuration object.')

    @classmethod
    def update_config(cls):
        """Handle any tweaks to the config that need to happen before
           register_config, but that can't be specified statically."""
        pass

    @classmethod
    def register_with_config(cls, oConfig):
        """Register this config class with the given config."""
        oConfig.add_plugin_specs(cls.__name__, cls.dGlobalConfig)
        oConfig.add_deck_specs(cls.__name__, cls.dPerPaneConfig)
        oConfig.add_cardlist_specs(cls.__name__, cls.dCardListConfig)
        oConfig.add_cardset_list_specs(cls.__name__, cls.dCardSetListConfig)

    @classmethod
    def check_versions(cls):
        """Check whether the plugin supports the current version of
           the Sutekh database tables."""
        oDBVer = DatabaseVersion()
        for oTable, aVersions in cls.dTableVersions.iteritems():
            if not oDBVer.check_table_in_versions(oTable, aVersions):
                logging.warn('Skipping plugin %s due to version error (%s)', cls, oTable)
                return False

        return True

    @classmethod
    def check_model_type(cls, cModelType):
        """Check whether the plugin should register on this frame."""
        if cModelType in cls.aModelsSupported:
            return True
        return False

    @classmethod
    def get_help_text(cls):
        """Return the help documentation for the plugin"""
        sText = getattr(cls, 'sHelpText', None)
        if sText:
            sText = ('\n').join([ x.strip() for x in sText.splitlines() ])
        return sText

    @classmethod
    def get_help_list_text(cls):
        """Return any additional text for list entries"""
        return ''

    @classmethod
    def get_help_numbered_text(cls):
        """Return any additional text for numbered entries"""
        return ''

    @classmethod
    def get_help_category(cls):
        """Return the help category to add this plugin to"""
        return getattr(cls, 'sHelpCategory', None)

    @classmethod
    def get_help_menu_entry(cls):
        """Return the menu name for the html help."""
        return getattr(cls, 'sMenuName', None)

    def add_to_menu(self, dAllMenus, oCatchAllMenu):
        """Grunt work of adding menu item to the frame"""
        aMenuItems = self.get_menu_item()
        if aMenuItems is not None:
            if not isinstance(aMenuItems, list):
                if not isinstance(aMenuItems, tuple):
                    aMenuItems = [('Plugins', aMenuItems)]
                else:
                    aMenuItems = [
                     aMenuItems]
            for sMenu, oMenuItem in aMenuItems:
                if sMenu in dAllMenus:
                    dAllMenus[sMenu].add(oMenuItem)
                else:
                    oCatchAllMenu.add(oMenuItem)

        return

    def get_config_item(self, sKey):
        """Return the value of a plugin global config key."""
        return self.config.get_plugin_key(self.__class__.__name__, sKey)

    def set_config_item(self, sKey, sValue):
        """Set the value of a plugin global config key."""
        self.config.set_plugin_key(self.__class__.__name__, sKey, sValue)

    def get_perpane_item(self, sKey):
        """Return the value of a per-pane config key."""
        oModel = self.model
        if oModel is None or not hasattr(oModel, 'cardset_id'):
            return
        if oModel.cardset_id == FULL_CARDLIST or oModel.cardset_id == CARDSET_LIST:
            sProfile = self.config.get_profile(oModel.cardset_id, oModel.cardset_id)
            return self.config.get_profile_option(oModel.cardset_id, sProfile, sKey)
        else:
            return self.config.get_deck_option(oModel.frame_id, oModel.cardset_id, sKey)

    def get_menu_item(self):
        """Return a list of ('Menu', gtk.MenuItems) pairs for the plugin or
           None if no menu item is needed."""
        return

    def setup(self):
        """Handle any setup needed for the plugin after the main window has
           been initialised.

           Currently used to prompt for downloads, etc.
           """
        return

    def cleanup(self):
        """Handle any cleanup needed by the plugin when the window or
           pane it's attached to goes away.

           Used for things like database signal cleanup, etc."""
        if self._oListener:
            self._oListener.cleanup()
        MessageBus.unsubscribe(DATABASE_MSG, 'update_to_new_db', self.update_to_new_db)
        MessageBus.unsubscribe(DATABASE_MSG, 'prepare_for_db_update', self.prepare_for_db_update)
        return

    def get_toolbar_widget(self):
        """Return an arbitary gtk.Widget which is added to a VBox between the
           menu and the scrolled display area.

           Return None is no toolbar Widget is needed
           """
        return

    def get_frame_from_config(self, _sType):
        """Hook for plugins which supply a frame in the Main window.

           Allows them to restore from the config file properly.
           """
        return

    def check_for_updates(self):
        """Called to check if the plugin has newer data to download.

           Should return a string with a message, or None if there's
           nothing to download."""
        return

    def do_update(self):
        """Called to handle any pending updates."""
        pass

    def perpane_config_updated(self, bDoReload=True):
        """Plugins should override this to be informed of config changes."""
        pass

    def update_to_new_db(self):
        """Plugins should override this to be informed of database changes."""
        pass

    def prepare_for_db_update(self):
        """Hook for any preparations needed before a database upgrade.

           Mainly useful for disconnecting database signals and such
           during a database upgrade"""
        pass

    def _open_cs(self, sPCS, bStartEditable=False):
        """Open a physical card set in the GUI."""
        self.parent.add_new_physical_card_set(sPCS, bStartEditable)

    def _reload_pcs_list(self):
        """Refresh the physical card set list if it is visible."""
        self.parent.reload_pcs_list()

    def _reload_all(self):
        """Reload all views."""
        self.parent.reload_all()

    def _get_card_set(self):
        """Get the Card Set for this view."""
        if self._cModelType is PhysicalCardSet:
            return self.model.cardset
        else:
            return

    def _get_selected_abs_cards(self):
        """Extract selected abstract cards from the selection."""
        aSelectedCards = []
        if self._cModelType in [PhysicalCardSet, PhysicalCard]:
            _oModel, aSelected = self.view.get_selection().get_selected_rows()
            for oPath in aSelected:
                oCard = IAbstractCard(self.model.get_card_name_from_path(oPath))
                aSelectedCards.append(oCard)

        return aSelectedCards

    def _get_all_cards(self):
        """Get the cards from the card set."""
        if self._cModelType is PhysicalCardSet:
            return self.model.get_card_iterator(None)
        else:
            return []

    def _check_cs_size(self, sName, iLimit):
        """Check that the card set isn't considerably larger than we
           expect to deal with and warn the user if it is"""
        iCards = 0
        aCards = self._get_all_cards()
        if aCards:
            iCards = aCards.count()
        if iCards > iLimit:
            iRes = do_complaint_warning("This card set is very large (%d cards), and so using the %s plugin doesn't seem sensible.\nAre you sure you want to continue?" % (
             iCards, sName))
            if iRes == gtk.RESPONSE_CANCEL:
                return False
        return True

    def _escape(self, sInput):
        """Escape strings so that markup and special characters don't break
           things."""
        if sInput:
            return markup_escape_text(sInput)
        return sInput

    def _commit_cards(self, oCS, aCards):
        """Add a list of physiccal cards to the given card set"""

        def _in_transaction(oCS, aCards):
            """The actual work happens here, so it can be wrapped in a
               sqlobject transaction"""
            for oCard in aCards:
                oCS.addPhysicalCard(oCard)

        sqlhub.doInTransaction(_in_transaction, oCS, aCards)