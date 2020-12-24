# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/api/domain_rbac.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 14, 2012\n\n@package: security RBAC\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Ioan v. Pocol\n\nProvides the decorator to be used by the models in the security RBAC domain.\n'
from ally.api.config import model
from functools import partial
DOMAIN = 'RBAC/'
modelRbac = partial(model, domain=DOMAIN)