# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/admin/api/domain_admin.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Apr 19, 2012

@package: administration support
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decorator to be used by the models in the admin domain.
"""
from functools import partial
from ally.api.config import model
DOMAIN = 'Admin/'
modelAdmin = partial(model, domain=DOMAIN)