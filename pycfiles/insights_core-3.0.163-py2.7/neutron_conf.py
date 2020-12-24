# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/neutron_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
NeutronConf - file ``/etc/neutron/neutron.conf``
================================================

This class provides parsing for the file ``/etc/neutron/neutron.conf``.

Sample input data is in the format::

    [DEFAULT]
    # debug = False
    debug = False
    # verbose = True
    verbose = False
    core_plugin =neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2

    [quotas]
    default_quota = -1
    quota_network = 10
    [agent]
    report_interval = 60

    [keystone_authtoken]
    auth_host = ost-controller-lb-del.om-l.dsn.inet
    auth_port = 35357

See the ``IniConfigFile`` class for examples.
"""
from .. import IniConfigFile, parser, add_filter
from insights.specs import Specs
add_filter(Specs.neutron_conf, ['['])

@parser(Specs.neutron_conf)
class NeutronConf(IniConfigFile):
    """Class to parse file ``neutron.conf``."""
    pass