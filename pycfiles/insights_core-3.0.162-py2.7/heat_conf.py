# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/heat_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
HeatConf - file ``/etc/heat/heat.conf``
=======================================

This module provides plugins access to the heat.conf information.

Typical content of the ``heat.conf`` is::

    [DEFAULT]
    heat_metadata_server_url = http://172.16.0.11:8000
    heat_waitcondition_server_url = http://172.16.0.11:8000/v1/waitcondition
    heat_watch_server_url =http://172.16.0.11:8003
    stack_user_domain_name = heat_stack
    stack_domain_admin = heat_stack_domain_admin
    stack_domain_admin_password = *********
    auth_encryption_key = V48p9fRZzWSRgjE96e2I1oGwn216xgqf
    log_dir = /var/log/heat
    instance_user=
    notification_driver=messaging
    [auth_password]
    [clients]
    [clients_ceilometer]
    [clients_cinder]
    [clients_glance]
    [clients_heat]
    [clients_keystone]
    auth_uri =http://192.0.2.18:35357
    [clients_neutron]

Usage of this parser is similar to others that use the ``IniConfigFile`` base
class.

Examples:

    >>> conf = shared(HeatConf)
    >>> 'DEFAULT' in conf
    True
    >>> conf.get_item('clients_keystone', 'auth_uri')
    'http://192.0.2.18:35357'
"""
from .. import parser, IniConfigFile
from insights.specs import Specs

@parser(Specs.heat_conf)
class HeatConf(IniConfigFile):
    """Parses content of "/etc/heat/heat.conf". """
    pass