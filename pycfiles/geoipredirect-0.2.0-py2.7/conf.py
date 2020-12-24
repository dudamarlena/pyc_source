# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/conf.py
# Compiled at: 2011-01-24 10:56:44
from django.conf import settings as core_settings
from geoip import settings as geo_settings

def geo_setting(conf_var):
    """ Tries returning a value from the main settings file
    or the defaults in geoip/settings.py or ultimately None """
    try:
        return getattr(core_settings, conf_var)
    except AttributeError:
        try:
            return getattr(geo_settings, conf_var)
        except AttributeError:
            return

    return