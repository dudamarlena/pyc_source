# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/api/domain_rbac.py
# Compiled at: 2013-04-24 04:53:27
"""
Created on Nov 14, 2012

@package: security RBAC
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Provides the decorator to be used by the models in the security RBAC domain.
"""
from ally.api.config import model
from functools import partial
DOMAIN = 'RBAC/'
modelRbac = partial(model, domain=DOMAIN)