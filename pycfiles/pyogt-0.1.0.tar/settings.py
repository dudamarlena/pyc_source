# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/settings.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from pyogp.lib.base.settings import Settings as BaseSettings

class Settings(BaseSettings):
    __module__ = __name__

    def __init__(self, quiet_logging=False, spammy_logging=False, log_tests=True):
        """ some lovely configurable settings 

        These are applied package wide, and can be
        overridden at any time in a specific instance

        This Settings instance inherits from pyogp.lib.base's settings
        """
        super(Settings, self).__init__(quiet_logging, spammy_logging, log_tests)
        self.DEFAULT_START_LOCATION = 'last'
        self.ENABLE_INVENTORY_MANAGEMENT = True
        self.ACCEPT_INVENTORY_OFFERS = False
        self.ENABLE_LIBRARY = True
        self.ENABLE_OBJECT_TRACKING = True
        self.ENABLE_COMMUNICATIONS_TRACKING = True
        self.ENABLE_GROUP_CHAT = True
        self.ENABLE_APPEARANCE_MANAGEMENT = True
        self.DEFAULT_CAMERA_DRAW_DISTANCE = 128
        self.DEFAULT_CAMERA_AT_AXIS = (1.0, 0.0, 0.0)
        self.DEFAULT_CAMERA_LEFT_AXIS = (0.0, 1.0, 0.0)
        self.DEFAULT_CAMERA_UP_AXIS = (0.0, 0.0, 1.0)
        self.INVENTORY_LOGIN_OPTIONS = [
         'inventory-root', 'inventory-skeleton', 'inventory-skel-lib']
        self.LIBRARY_LOGIN_OPTIONS = [
         'inventory-lib-root', 'inventory-lib-owner']
        self.ALEXANDRIA_LINDEN = 'ba2a564a-f0f1-4b82-9c61-b7520bfcd09f'
        self.ENABLE_EXTENDED_LOGIN_OPTIONS = False
        self.EXTENDED_LOGIN_OPTIONS = ['gestures', 'event_categories', 'event_notifications', 'classified_categories', 'buddy-list', 'ui-config', 'login-flags', 'global-textures']
        self.ENABLE_REGION_EVENT_QUEUE = True
        self.HANDLE_EVENT_QUEUE_DATA = True
        self.MULTIPLE_SIM_CONNECTIONS = False
        self.ENABLE_PARCEL_TRACKING = True
        self.AGENT_UPDATES_PER_SECOND = 10
        self.ENABLE_AGENTDOMAIN_EVENT_QUEUE = True
        self.AGENT_DOMAIN_EVENT_QUEUE_POLL_INTERVAL = 15
        if log_tests:
            self.ENABLE_LOGGING_IN_TESTS = True
        else:
            self.ENABLE_LOGGING_IN_TESTS = False

    def get_default_xmlrpc_login_parameters(self):
        """ returns some default login params """
        login_options = []
        if self.ENABLE_INVENTORY_MANAGEMENT:
            for option in self.INVENTORY_LOGIN_OPTIONS:
                login_options.append(option)

        if self.ENABLE_LIBRARY:
            for option in self.LIBRARY_LOGIN_OPTIONS:
                login_options.append(option)

        if self.ENABLE_EXTENDED_LOGIN_OPTIONS:
            for option in self.EXTENDED_LOGIN_OPTIONS:
                login_options.append(option)

        params = {'major': '1', 'minor': '22', 'patch': '9', 'build': '1', 'platform': 'Win', 'options': login_options, 'user-agent': 'pyogp 0.1', 'id0': '', 'viewer_digest': '09d93740-8f37-c418-fbf2-2a78c7b0d1ea', 'version': 'pyogp 0.1', 'channel': 'pyogp', 'mac': '', 'agree_to_tos': True, 'read_critical': True}
        return params