# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frontline/api/domain_sms.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on April 24, 2013

@package: frontline
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Martin Saturka

Provides the decorator to be used by the models in the frontline domain.
"""
from ally.api.config import model
from functools import partial
DOMAIN = 'SMS/'
modelSMS = partial(model, domain=DOMAIN)