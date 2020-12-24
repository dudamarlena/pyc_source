# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/keystone.py
# Compiled at: 2019-05-16 13:41:33
"""
KeystoneConf - file ``/etc/keystone/keystone.conf``
===================================================

The ``KeystoneConf`` class parses the information in the file
``/etc/keystone/keystone.conf``.  See the ``IniConfigFile`` class for more
information on attributes and methods.

Sample input data looks like::

    [DEFAULT]

    #
    # From keystone
    #
    admin_token = ADMIN
    compute_port = 8774

    [identity]

    # From keystone
    default_domain_id = default
    #domain_specific_drivers_enabled = false
    domain_configurations_from_database = false

    [identity_mapping]

    driver = keystone.identity.mapping_backends.sql.Mapping
    generator = keystone.identity.id_generators.sha256.Generator
    #backward_compatible_ids = true

Examples:

    >>> kconf = shared[KeystoneConf]
    >>> kconf.defaults()
    {'admin_token': 'ADMIN', 'compute_port': '8774'}
    >>> 'identity' in kconf
    True
    >>> kconf.has_option('identity', 'default_domain_id')
    True
    >>> kconf.has_option('identity', 'domain_specific_drivers_enabled')
    False
    >>> kconf.get('identity', 'default_domain_id')
    'default'
    >>> kconf.items('identity_mapping')
    {'driver': 'keystone.identity.mapping_backends.sql.Mapping',
     'generator': 'keystone.identity.id_generators.sha256.Generator'}
"""
from .. import IniConfigFile, parser
from insights.specs import Specs

@parser(Specs.keystone_conf)
class KeystoneConf(IniConfigFile):
    """Parse contents of file ``/etc/keystone/keystone.conf``."""
    pass