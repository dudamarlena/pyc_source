# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/superdesk_security/patch_ally_core.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 26, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core setup patch.
"""
from .service import assemblyGateways, updateAssemblyGateways, registerMethodOverride, updateAssemblyActiveRights, assemblyActiveRights, registerDefaultRights, userValueForFilter
from ally.container import support, ioc
import logging
log = logging.getLogger(__name__)
try:
    from __setup__ import ally_core
except ImportError:
    log.info('No ally core component available, thus cannot populate processors')
else:
    ally_core = ally_core
    from acl.core.impl.processor import resource_node_associate, resource_model_filter, resource_alternate, resource_gateway
    iterateResourcePermissions = checkResourceAvailableRights = modelFiltersForPermissions = authenticatedForPermissions = alternateNavigationPermissions = gatewaysFromPermissions = support.notCreated
    support.createEntitySetup(resource_node_associate, resource_model_filter, resource_alternate, resource_gateway)

    @ioc.after(updateAssemblyGateways)
    def updateAssemblyGatewaysForResources():
        assemblyGateways().add(iterateResourcePermissions(), authenticatedForPermissions(), userValueForFilter(), alternateNavigationPermissions(), gatewaysFromPermissions(), before=registerMethodOverride())


    @ioc.after(updateAssemblyActiveRights)
    def updateAssemblyActiveRightsForResources():
        assemblyActiveRights().add(checkResourceAvailableRights(), after=registerDefaultRights())