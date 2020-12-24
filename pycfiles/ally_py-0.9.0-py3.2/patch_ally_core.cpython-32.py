# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/captcha/patch_ally_core.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 26, 2013

@package: captcha
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core setup patch.
"""
from .service import assemblyCaptchaGateways, updateAssemblyCaptchaGateways
from ally.container import support, ioc
import logging
log = logging.getLogger(__name__)
try:
    from __setup__ import ally_core
except ImportError:
    log.info('No ally core component available, thus cannot populate captcha gateway processors')
else:
    from acl.core.impl.processor import resource_node_associate, resource_gateway
    iterateResourcePermissions = gatewaysFromPermissions = support.notCreated
    support.createEntitySetup(resource_node_associate.IterateResourcePermissions, resource_gateway.GatewaysFromPermissions)

    @ioc.after(updateAssemblyCaptchaGateways)
    def updateAssemblyCaptchaGatewaysForResources():
        assemblyCaptchaGateways().add(iterateResourcePermissions(), gatewaysFromPermissions())