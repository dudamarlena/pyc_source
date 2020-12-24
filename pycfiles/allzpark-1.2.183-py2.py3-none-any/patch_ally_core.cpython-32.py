# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/captcha/patch_ally_core.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 26, 2013\n\n@package: captcha\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the ally core setup patch.\n'
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