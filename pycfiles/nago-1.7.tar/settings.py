# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/nago/nago/extensions/settings.py
# Compiled at: 2013-12-04 13:14:57
""" Manage settings on a local node """
import nago.settings
from nago.core import nago_access

@nago_access(name='set')
def edit_settings(section='main', **kwargs):
    """ Change a single option in local configuration """
    return nago.settings.set_option(section, **kwargs)


@nago_access(name='get')
def get(key, section='main'):
    """ Get a single option from """
    return nago.settings.get_option(option_name=key, section_name=section)