# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/raton/pycharm_projects/django-hautomation-suite/django_hautomation_suite/ha_cfg/paths.py
# Compiled at: 2014-06-30 03:45:01
import os

def x10_plugin_settings():
    import hautomation_x10
    p = os.path.join(os.path.dirname(hautomation_x10.__file__), 'settings.py')
    if not os.path.isfile(p):
        raise ValueError('Cannot find X10 plugin settings file')
    return p


def django_thermostat_settings():
    import django_thermostat
    p = os.path.join(os.path.dirname(django_thermostat.__file__), 'settings.py')
    if not os.path.isfile(p):
        raise ValueError('Cannot find django_thermostat settings file')
    return p