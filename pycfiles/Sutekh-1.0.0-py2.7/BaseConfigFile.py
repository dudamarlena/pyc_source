# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BaseConfigFile.py
# Compiled at: 2019-12-11 16:37:48
"""Base classes and constants for configuation management."""
import datetime, pkg_resources
from configobj import ConfigObj, flatten_errors
from validate import Validator, is_option, is_list, VdtTypeError
from .MessageBus import MessageBus, CONFIG_MSG
CARDSET = 'Card Set'
FRAME = 'Frame'
FULL_CARDLIST = 'cardlist'
CARDSET_LIST = 'cardset list'
DEF_PROFILE_FILTER = 'No profile filter'

def is_option_list(sValue, *aOptions):
    """Validator function for option_list configspec type."""
    return [ is_option(sMem, *aOptions) for sMem in is_list(sValue) ]


def is_date_format(sValue):
    """Validator function to check for date format."""
    try:
        oDate = datetime.datetime.strptime(sValue, '%Y-%m-%d').date()
    except ValueError:
        raise VdtTypeError(sValue)

    return oDate


class BaseConfigFile(object):
    """Handle the setup and management of the config file.

       Ensure that the needed sections exist, and that sensible
       defaults values are assigned.

       Filters are saved to the config file, and interested objects
       can register as listeners on the config file to respond to
       changes to the filters.
       """
    dCustomConfigTypes = {'option_list': is_option_list, 
       'date': is_date_format}
    DEFAULT_FILTERS = {}

    def __init__(self, sFileName):
        self._sFileName = sFileName
        self._bWriteable = False
        self._oConfigSpec = None
        self._oConfig = None
        self._dLocalFrameOptions = {}
        self._oValidator = None
        self._dPluginSpecs = {}
        self._dDeckSpecs = {}
        self._dCardListSpecs = {}
        self._dCardSetListSpecs = {}
        return

    def __str__(self):
        """Debugging aid - include the filename"""
        return '<%s object at %s; config file: %r>' % (
         self.__class__.__name__, hex(id(self)), self._sFileName)

    def add_plugin_specs(self, sName, dConfigSpecs):
        """Add a validator to the plugins_main configspec section."""
        self._dPluginSpecs[sName] = dConfigSpecs

    def add_deck_specs(self, sName, dConfigSpecs):
        """Add validation options to the per_deck.defaults configspec."""
        self._dDeckSpecs[sName] = dConfigSpecs

    def add_cardlist_specs(self, sName, dConfigSpecs):
        """Add validation options to the cardlist configspec."""
        self._dCardListSpecs[sName] = dConfigSpecs

    def add_cardset_list_specs(self, sName, dConfigSpecs):
        """Add validation options to the cardset list configspec."""
        self._dCardSetListSpecs[sName] = dConfigSpecs

    def _get_app_configspec_file(self):
        """Get the application specific config spec file.

           Return None if there's no extension to the base configspec"""
        raise NotImplementedError

    def validate(self):
        """Validate a configuration object."""
        fConfigSpec = pkg_resources.resource_stream(__name__, 'baseconfigspec.ini')
        oConfigSpec = ConfigObj(fConfigSpec, raise_errors=True, file_error=True, list_values=False, encoding='utf8')
        fAppConfigSpec = self._get_app_configspec_file()
        if fAppConfigSpec:
            oAppConfigSpec = ConfigObj(fAppConfigSpec, raise_errors=True, file_error=True, list_values=False, encoding='utf8')
            oConfigSpec.merge(oAppConfigSpec)
        for sPlugin, dGlobal in self._dPluginSpecs.items():
            oConfigSpec['plugins_main'][sPlugin] = dGlobal

        for sPlugin, dPerDeck in self._dDeckSpecs.items():
            for sKey, oValue in dPerDeck.items():
                oConfigSpec['per_deck']['defaults'][sKey] = oValue

        for sPlugin, dGlobal in self._dCardListSpecs.items():
            for sKey, oValue in dGlobal.items():
                oConfigSpec['cardlist']['defaults'][sKey] = oValue

        for sPlugin, dGlobal in self._dCardSetListSpecs.items():
            for sKey, oValue in dGlobal.items():
                oConfigSpec['cardset list']['defaults'][sKey] = oValue

        for sKey, oValue in oConfigSpec['cardlist']['defaults'].items():
            oConfigSpec['cardlist']['profiles']['__many__'][sKey] = oValue

        for sKey, oValue in oConfigSpec['cardset list']['defaults'].items():
            oConfigSpec['cardset list']['profiles']['__many__'][sKey] = oValue

        for sKey, oValue in oConfigSpec['per_deck']['defaults'].items():
            oConfigSpec['per_deck']['profiles']['__many__'][sKey] = oValue

        self._oConfigSpec = oConfigSpec
        self._oConfig = ConfigObj(self._sFileName, configspec=oConfigSpec, indent_type='    ', encoding='utf8')
        self.update_filter_list()
        self._oValidator = Validator(self.dCustomConfigTypes)
        oResults = self._oConfig.validate(self._oValidator, preserve_errors=True)
        self._fix_filter_defaults()
        return oResults

    def update_filter_list(self):
        """Add/Update a option validator for the filters.

           This is so the profile editor lists things sensibly."""
        try:
            aValidProfileFilters = self._oConfig['filters'].keys()
        except KeyError:
            aValidProfileFilters = []

        aValidProfileFilters.append(DEF_PROFILE_FILTER)
        for sType in ['per_deck', FULL_CARDLIST]:
            self._oConfigSpec[sType]['defaults']['filter'] = 'option(%s, default=%s)' % ((', ').join(aValidProfileFilters),
             DEF_PROFILE_FILTER)
            self._oConfigSpec[sType]['profiles']['__many__']['filter'] = 'option(%s, default=%s)' % ((', ').join(aValidProfileFilters),
             DEF_PROFILE_FILTER)

    def _fix_filter_defaults(self):
        """Ensure we are set in the default profile if needed"""
        for sType in ['per_deck', FULL_CARDLIST]:
            if 'filter' not in self._oConfig[sType]['defaults']:
                self._oConfig[sType]['defaults']['filter'] = DEF_PROFILE_FILTER

    def validation_errors(self, oValidationResults):
        """Return a list of string describing any validation errors.

           Returns an empty list if no validation errors occurred. Validation
           results must have been returned by a call to validate() on the same
           config object.
           """
        aErrors = []
        if oValidationResults is True:
            return aErrors
        else:
            for aSections, sKey, _oIgnore in flatten_errors(self._oConfig, oValidationResults):
                if sKey is not None:
                    aErrors.append('Key %r in section %r failed validation.' % (
                     sKey, aSections))
                else:
                    aErrors.append('Section %r was missing.' % (aSections,))

            return aErrors

    def get_validator(self):
        """Return the validator used to check the configuration."""
        return self._oValidator

    def sanitize(self):
        """Called after validation to clean up a valid config.
           """
        raise NotImplementedError

    def check_writeable(self):
        """Test that we can open the file for writing"""
        self._bWriteable = True
        try:
            oFile = open(self._sFileName, 'a')
            oFile.close()
        except IOError:
            self._bWriteable = False

        return self._bWriteable

    def write(self):
        """Write the config file to disk."""
        if self._bWriteable:
            self._oConfig.write()

    def clear_open_frames(self):
        """Clear out old save panes (used before adding new ones)."""
        self._oConfig['open_frames'].clear()

    def open_frames(self):
        """Get the all the panes saved in the config file, and their
           positions."""
        aRes = []
        for sKey, dPane in self._oConfig['open_frames'].items():
            if not sKey.startswith('pane'):
                continue
            try:
                iPaneNumber = int(sKey.split(' ')[1])
            except ValueError:
                continue

            iPos = dPane['position']
            if dPane['orientation'] == 'C':
                iPos = 0
            aRes.append((
             iPaneNumber,
             dPane['type'],
             dPane['name'],
             dPane['paneid'],
             dPane['orientation'] == 'V',
             dPane['orientation'] == 'C',
             iPos))

        aRes.sort()
        return aRes

    def update_pane_numbers(self, dPaneMap):
        """Update the profiles to reflect changes in pane-id.

           dPaneMap is a dictionary mapping old_id -> new_id"""
        dOldProfiles = self._oConfig['per_deck']['frame_profiles'].copy()
        for sId in dOldProfiles:
            self.set_profile(FRAME, sId, None)

        for sOldId, sNewId in dPaneMap.iteritems():
            if sOldId in dOldProfiles:
                self.set_profile(FRAME, sNewId, dOldProfiles[sOldId])

        return

    def add_frame(self, iFrameNumber, sType, sName, bVertical, bClosed, iPos, sPaneId):
        """Add a frame with the given position info to the config file"""
        oPanes = self._oConfig['open_frames']
        sKey = 'pane %d' % iFrameNumber
        oPanes[sKey] = {}
        oNewPane = oPanes[sKey]
        oNewPane['type'] = sType
        oNewPane['name'] = sName
        oNewPane['paneid'] = sPaneId
        if bVertical:
            oNewPane['orientation'] = 'V'
        elif bClosed:
            oNewPane['orientation'] = 'C'
        else:
            oNewPane['orientation'] = 'H'
        if iPos > 0 and self.get_save_precise_pos() and not bClosed:
            oNewPane['position'] = iPos
        elif bClosed:
            oNewPane['position'] = 0
        else:
            oNewPane['position'] = -1

    def get_plugin_key(self, sPlugin, sKey):
        """Get an option from the plugins section.

           Return None if no option is set
           """
        try:
            sResult = self._oConfig['plugins_main'][sPlugin][sKey]
        except KeyError:
            sResult = None

        return sResult

    def set_plugin_key(self, sPlugin, sKey, sValue, bCreateSection=False):
        """Set a value in the plugin section"""
        if bCreateSection and sPlugin not in self._oConfig['plugins_main']:
            self._oConfig['plugins_main'][sPlugin] = {}
        self._oConfig['plugins_main'][sPlugin][sKey] = sValue

    def get_filters(self):
        """Get all the filters in the config file.

           Filters are return as a list of (sQuery, dVars) tuples.
           """
        return [ (oF['query'], oF['vars']) for oF in self._oConfig['filters'].values()
               ]

    def get_default_filters(self):
        """Return the default filter list."""
        return self.DEFAULT_FILTERS

    def get_filter_keys(self):
        """Return all the keys for all the filters in the config file."""
        return [ (sKey, dFilter['query']) for sKey, dFilter in self._oConfig['filters'].items()
               ]

    def get_profiles_for_filter(self, sMatchFilter):
        """Return a dictionary of profiles currently using the given filter"""
        dProfileFilters = {}
        for sType in [CARDSET, FULL_CARDLIST]:
            dProfileFilters[sType] = []
            if sType == CARDSET:
                dConfig = self._oConfig['per_deck']
            else:
                dConfig = self._oConfig[sType]
            sFilter = dConfig['defaults'].get('filter', DEF_PROFILE_FILTER)
            if sFilter == sMatchFilter:
                dProfileFilters[sType].append('defaults')
            for sProfile in dConfig['profiles']:
                sFilter = dConfig['profiles'][sProfile].get('filter', DEF_PROFILE_FILTER)
                if sFilter == sMatchFilter:
                    dProfileFilters[sType].append(sProfile)

        return dProfileFilters

    def get_filter(self, sKey):
        """Return the filter associated with the given key.

           Return None if the filter is not known.
           """
        sKey = sKey.lower()
        if sKey in self._oConfig['filters']:
            return self._oConfig['filters'][sKey]['query']
        else:
            return

    def get_filter_values(self, sKey):
        """Return the filter values associated with the given key.

        Return None if the filter is not knonw.
        """
        sKey = sKey.lower()
        if sKey in self._oConfig['filters']:
            return self._oConfig['filters'][sKey]['vars'].dict()
        else:
            return

    def add_filter(self, sKey, sQuery, dVars={}):
        """Add a filter to the config file."""
        sKey = sKey.lower()
        if sKey not in self._oConfig['filters']:
            dFilter = {'query': sQuery, 'vars': dVars}
            self._oConfig['filters'][sKey] = dFilter
            MessageBus.publish(CONFIG_MSG, 'add_filter', sKey, sQuery)

    def remove_filter(self, sKey, sFilter):
        """Remove a filter from the file"""
        sKey = sKey.lower()
        if sKey in self._oConfig['filters'] and sFilter == self._oConfig['filters'][sKey]['query']:
            del self._oConfig['filters'][sKey]
            MessageBus.publish(CONFIG_MSG, 'remove_filter', sKey, sFilter)
            dProfileFilters = self.get_profiles_for_filter(sKey)
            for sType in dProfileFilters:
                aProfiles = dProfileFilters[sType]
                for sProfile in aProfiles:
                    if sProfile == 'defaults':
                        self.set_profile_option(sType, None, 'filter', DEF_PROFILE_FILTER)
                    else:
                        self.set_profile_option(sType, sProfile, 'filter', DEF_PROFILE_FILTER)

        return

    def replace_filter(self, sKey, sOldFilter, sNewFilter):
        """Replace a filter in the file with new filter"""
        sKey = sKey.lower()
        if sKey in self._oConfig['filters'] and sOldFilter == self._oConfig['filters'][sKey]['query']:
            self._oConfig['filters'][sKey]['query'] = sNewFilter
            MessageBus.publish(CONFIG_MSG, 'replace_filter', sKey, sOldFilter, sNewFilter)

    def get_deck_option(self, sFrame, sCardset, sKey, bUseLocal=True):
        """Retrieve the value of a per-deck option.

           Either sFrame or sCardset may be None, in
           which case the frame or cardset option look-up
           is skipped.
           """
        try:
            if bUseLocal:
                return self._dLocalFrameOptions[sFrame][sKey]
        except KeyError:
            pass

        dPerDeck = self._oConfig['per_deck']
        try:
            sProfile = dPerDeck['frame_profiles'][sFrame]
            return dPerDeck['profiles'][sProfile][sKey]
        except KeyError:
            pass

        try:
            sProfile = dPerDeck['cardset_profiles'][sCardset]
            return dPerDeck['profiles'][sProfile][sKey]
        except KeyError:
            pass

        return dPerDeck['defaults'][sKey]

    def get_deck_profile_option(self, sProfile, sKey):
        """Get the value of a per-deck option for a profile."""
        try:
            if sProfile is None:
                return self._oConfig['per_deck']['defaults'][sKey]
            else:
                return self._oConfig['per_deck']['profiles'][sProfile][sKey]

        except KeyError:
            return

        return

    def get_local_frame_option(self, sFrame, sKey):
        """Get the value of a per-deck option for a local frame."""
        try:
            return self._dLocalFrameOptions[sFrame][sKey]
        except KeyError:
            return

        return

    def set_profile_option(self, sType, sProfile, sKey, sValue):
        """Set the value of a option for a profile for sType.

           If sValue is None, remove the key. New profiles are
           created as needed.
           """
        if sType == CARDSET:
            dConfig = self._oConfig['per_deck']
        else:
            dConfig = self._oConfig[sType]
        if sProfile is None:
            dProfile = dConfig['defaults']
        elif sProfile in dConfig['profiles']:
            dProfile = dConfig['profiles'][sProfile]
        else:
            dConfig['profiles'][sProfile] = {}
            dProfile = dConfig['profiles'][sProfile]
        bChanged = False
        if sValue is None:
            if sKey in dProfile:
                bChanged = True
                del dProfile[sKey]
        elif sKey not in dProfile or dProfile[sKey] != sValue:
            bChanged = True
            dProfile[sKey] = sValue
        if bChanged:
            MessageBus.publish(CONFIG_MSG, 'profile_option_changed', sType, sProfile, sKey)
        return

    def set_local_frame_option(self, sFrame, sKey, sValue):
        """Set the value of an option in the local frame option dictionary.

        If sValue is None, remove the key.
        """
        if sFrame in self._dLocalFrameOptions:
            dOptions = self._dLocalFrameOptions[sFrame]
        else:
            dOptions = {}
            self._dLocalFrameOptions[sFrame] = dOptions
        bChanged = False
        if sValue is None:
            if sKey in dOptions:
                bChanged = True
                del dOptions[sKey]
        elif sKey not in dOptions or dOptions[sKey] != sValue:
            bChanged = True
            dOptions[sKey] = sValue
        if bChanged:
            MessageBus.publish(CONFIG_MSG, 'profile_changed', FRAME, sFrame)
        return

    def clear_frame_profile(self, sId):
        """Clear any pane profiles set for this frame"""
        dProfiles = self._oConfig['per_deck']['frame_profiles']
        if sId in dProfiles:
            del dProfiles[sId]

    def clear_cardset_profile(self, sId):
        """Clear any profiles set for this cardset"""
        dProfiles = self._oConfig['per_deck']['cardset_profiles']
        if sId in dProfiles:
            del dProfiles[sId]

    def fix_profile_mapping(self, dOldMap, dNewMap):
        """Update the card set profiles to a new id -> name mapping"""
        dNewRev = dict(zip(dNewMap.itervalues(), dNewMap.iterkeys()))
        dOldProfiles = self._oConfig['per_deck']['cardset_profiles'].copy()
        dProfiles = self._oConfig['per_deck']['cardset_profiles']
        dProfiles.clear()
        for sId, sProfile in dOldProfiles.iteritems():
            iId = int(sId[2:])
            if iId not in dOldMap:
                continue
            sName = dOldMap[iId]
            if sName in dNewRev:
                sNewId = 'cs%d' % dNewRev[sName]
                dProfiles[sNewId] = sProfile

    def set_profile(self, sType, sId, sProfile):
        """Set the profile associated of the given type."""
        if sType == CARDSET or sType == FRAME:
            if sType == CARDSET:
                dProfiles = self._oConfig['per_deck']['cardset_profiles']
            else:
                dProfiles = self._oConfig['per_deck']['frame_profiles']
            if dProfiles.get(sId) == sProfile:
                return
            if sProfile is None:
                del dProfiles[sId]
            else:
                dProfiles[sId] = sProfile
        elif sType == FULL_CARDLIST and sId == FULL_CARDLIST or sType == CARDSET_LIST and sId == CARDSET_LIST:
            sCurProfile = self._oConfig[sType].get('current profile')
            if sCurProfile == sProfile:
                return
            if sProfile is None:
                del self._oConfig[sType]['current profile']
            else:
                self._oConfig[sType]['current profile'] = sProfile
        else:
            return
        MessageBus.publish(CONFIG_MSG, 'profile_changed', sType, sId)
        return

    def get_profile(self, sType, sId):
        """Return the current profile of the cardset/cardlist/cardset list."""
        if sType == CARDSET:
            return self._oConfig['per_deck']['cardset_profiles'].get(sId)
        else:
            if sType == FRAME:
                return self._oConfig['per_deck']['frame_profiles'].get(sId)
            if sType == FULL_CARDLIST and sId == FULL_CARDLIST or sType == CARDSET_LIST and sId == CARDSET_LIST:
                return self._oConfig[sType].get('current profile')
            return

    def clear_profiles(self, sType, sProfile):
        """Find all cardsets/frames using this profile, and change them to
          the default"""
        if sType == CARDSET or sType == FRAME:
            if sType == CARDSET:
                dProfiles = self._oConfig['per_deck']['cardset_profiles']
            else:
                dProfiles = self._oConfig['per_deck']['frame_profiles']
            for sId, sCurProfile in dProfiles.items():
                if sCurProfile == sProfile:
                    self.set_profile(sType, sId, None)

        else:
            sCurProfile = self._oConfig[sType].get('current profile')
            if sCurProfile == sProfile:
                self.set_profile(sType, sType, None)
        return

    def remove_profile(self, sType, sProfile):
        """Remove a profile from the file"""
        dData = {}
        if sType == FRAME or sType == CARDSET:
            dData = self._oConfig['per_deck']['profiles']
        elif sType == CARDSET_LIST:
            dData = self._oConfig['cardset list']['profiles']
        elif sType == FULL_CARDLIST:
            dData = self._oConfig['cardlist']['profiles']
        if sProfile in dData:
            if sType == FRAME or sType == CARDSET:
                self.clear_profiles(FRAME, sProfile)
                self.clear_profiles(CARDSET, sProfile)
            else:
                self.clear_profiles(sType, sProfile)
            del dData[sProfile]
            MessageBus.publish(CONFIG_MSG, 'remove_profile', sType, sProfile)

    def frame_profiles(self):
        """Return a dictionary of frame id -> profile mappings."""
        return dict(self._oConfig['per_deck']['frame_profiles'])

    def get_profile_users(self, sType, sProfile):
        """Returns a list of all card sets or panes that use the
           given profile"""
        if sType == CARDSET_LIST:
            sCurProfile = self._oConfig[sType].get('current profile')
            if sCurProfile == sProfile:
                return ['Card Set List']
        elif sType == FULL_CARDLIST:
            sCurProfile = self._oConfig[sType].get('current profile')
            if sCurProfile == sProfile:
                return ['Full Card List']
        elif sType == CARDSET:
            aUsers = []
            for dProfiles in (self._oConfig['per_deck']['cardset_profiles'], self._oConfig['per_deck']['frame_profiles']):
                for sId, sCurProfile in dProfiles.iteritems():
                    if sProfile == sCurProfile:
                        aUsers.append(sId)

            return aUsers
        return

    def profiles(self, sType):
        """Return a list of profile keys."""
        if sType == FRAME or sType == CARDSET:
            return list(self._oConfig['per_deck']['profiles'].keys())
        else:
            if sType == CARDSET_LIST:
                return list(self._oConfig['cardset list']['profiles'].keys())
            if sType == FULL_CARDLIST:
                return list(self._oConfig['cardlist']['profiles'].keys())
            return

    def profile_options(self, sType):
        """Return a list of per-deck option names."""
        if sType == FRAME or sType == CARDSET:
            return self._oConfig['per_deck']['defaults'].keys()
        return self._oConfig[sType]['defaults'].keys()

    def get_option_spec(self, sType, sKey):
        """Return the config spec for a given option."""
        if sType == FRAME or sType == CARDSET:
            return self._oConfigSpec['per_deck']['defaults'][sKey]
        return self._oConfigSpec[sType]['defaults'][sKey]

    def get_profile_option(self, sType, sProfile, sKey):
        """Get the value of a per-deck option for a profile."""
        if sType == FRAME or sType == CARDSET:
            return self.get_deck_profile_option(sProfile, sKey)
        else:
            try:
                if sProfile is None or sProfile.lower() == 'default':
                    return self._oConfig[sType]['defaults'][sKey]
                try:
                    return self._oConfig[sType]['profiles'][sProfile][sKey]
                except KeyError:
                    return self._oConfig[sType]['defaults'][sKey]

            except KeyError:
                return

            return

    def get_save_on_exit(self):
        """Query the 'save on exit' option."""
        return self._oConfig['main']['save on exit']

    def set_save_on_exit(self, bSaveOnExit):
        """Set the 'save on exit' option."""
        self._oConfig['main']['save on exit'] = bSaveOnExit

    def get_check_for_updates(self):
        """Query the 'check for updates on startup' option."""
        return self._oConfig['main']['check for updates on startup']

    def set_check_for_updates(self, bCheck):
        """Query the 'check for updates on startup' option."""
        self._oConfig['main']['check for updates on startup'] = bCheck

    def get_save_precise_pos(self):
        """Query the 'save pane sizes' option."""
        return self._oConfig['main']['save pane sizes']

    def set_save_precise_pos(self, bSavePos):
        """Set the 'save pane sizes' option."""
        self._oConfig['main']['save pane sizes'] = bSavePos

    def get_save_window_size(self):
        """Query the 'save window size' option."""
        return self._oConfig['main']['save window size']

    def set_save_window_size(self, bSavePos):
        """Set the 'save window size' option."""
        self._oConfig['main']['save window size'] = bSavePos

    def set_database_uri(self, sDatabaseURI):
        """Set the configured database URI"""
        self._oConfig['main']['database url'] = sDatabaseURI

    def get_database_uri(self):
        """Get database URI from the config file"""
        return self._oConfig['main']['database url']

    def get_icon_path(self):
        """Get the icon path from the config file"""
        return self._oConfig['main']['icon path']

    def set_icon_path(self, sPath):
        """Set the configured icon path"""
        self._oConfig['main']['icon path'] = sPath

    def get_window_size(self):
        """Get the saved window size from the config file."""
        iWidth, iHeight = self._oConfig['main']['window size']
        return (iWidth, iHeight)

    def set_window_size(self, tSize):
        """Save the current window size."""
        self._oConfig['main']['window size'] = tSize

    def get_postfix_the_display(self):
        """Get the 'postfix name display' option."""
        return self._oConfig['main']['postfix name display']

    def set_postfix_the_display(self, bPostfix):
        """Set the 'postfix name display' option."""
        self._oConfig['main']['postfix name display'] = bPostfix
        MessageBus.publish(CONFIG_MSG, 'set_postfix_the_display', bPostfix)

    def get_socket_timeout(self):
        """Get the timeout config value"""
        return self._oConfig['main']['socket timeout']