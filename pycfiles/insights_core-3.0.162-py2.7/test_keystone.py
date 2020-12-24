# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_keystone.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.keystone import KeystoneConf
from insights.tests import context_wrap
KEYSTONE_CONF = ('\n[DEFAULT]\n\n#\n# From keystone\n#\nadmin_token = ADMIN\ncompute_port = 8774\n\n[identity]\n\n# From keystone\ndefault_domain_id = default\n#domain_specific_drivers_enabled = false\ndomain_configurations_from_database = false\n\n[identity_mapping]\n\ndriver = keystone.identity.mapping_backends.sql.Mapping\ngenerator = keystone.identity.id_generators.sha256.Generator\n#backward_compatible_ids = true\n').strip()

def test_keystone():
    kconf = KeystoneConf(context_wrap(KEYSTONE_CONF))
    assert kconf is not None
    assert kconf.defaults() == {'admin_token': 'ADMIN', 'compute_port': '8774'}
    assert 'identity' in kconf
    assert 'identity_mapping' in kconf
    assert kconf.has_option('identity', 'default_domain_id')
    assert kconf.has_option('identity_mapping', 'driver')
    assert not kconf.has_option('identity', 'domain_specific_drivers_enabled')
    assert kconf.get('identity', 'default_domain_id') == 'default'
    assert kconf.items('DEFAULT') == {'admin_token': 'ADMIN', 'compute_port': '8774'}
    return