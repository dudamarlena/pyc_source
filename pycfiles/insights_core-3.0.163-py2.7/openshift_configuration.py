# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/openshift_configuration.py
# Compiled at: 2019-05-16 13:41:33
"""
openshift configuration files
=============================

``/etc/origin/node/node-config.yaml`` and
``/etc/origin/master/master-config.yaml`` are configuration files of
openshift Master node and Node node. Their format are both ``yaml``.

OseNodeConfig - file ``/etc/origin/node/node-config.yaml``
----------------------------------------------------------

Reads the OpenShift node configuration

OseMasterConfig - file ``/etc/origin/master/master-config.yaml``
----------------------------------------------------------------

Reads the Openshift master configuration

Examples:
    >>> result = shared[OseMasterConfig]
    >>> result.data['assetConfig']['masterPublicURL']
    'https://master.ose.com:8443'
    >>> result.data['corsAllowedOrigins'][1]
    'localhost'
"""
from .. import YAMLParser, parser
from insights.specs import Specs

@parser(Specs.ose_node_config)
class OseNodeConfig(YAMLParser):
    """Class to parse ``/etc/origin/node/node-config.yaml``"""
    pass


@parser(Specs.ose_master_config)
class OseMasterConfig(YAMLParser):
    """Class to parse ``/etc/origin/master/master-config.yaml``"""
    pass