# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/adspanel/config.py
# Compiled at: 2008-01-13 10:18:33
from trac.core import *
from trac.config import Option, BoolOption

class AdsPanelOptions(Component):
    hide_for_authenticated = BoolOption('adspanel', 'hide_for_authenticated', True, 'Should the ads be hidden for authenticated users.')
    ads_code = Option('adspanel', 'ads_code', None, 'The HTML code which displays the ads.\n\n        NOTE: You are responsible for the HTML code you add.')
    store_in_session = BoolOption('adspanel', 'store_in_session', True, "Should the hidden/shown status be stored in session. If True,\n        a user returning won't ever see the ads again until session is\n        invalidated or user visits\n        `http://domain.tld/<script_path>/adspanel/show`")