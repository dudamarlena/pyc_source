# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/api/domain_superdesk.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Apr 19, 2012

@package: superdesk
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decorator to be used by the models in the superdesk domain.
"""
from functools import partial
from ally.api.config import model
DOMAIN_LOCALIZATION = 'Localization/'
modelLocalization = partial(model, domain=DOMAIN_LOCALIZATION)
DOMAIN = 'HR/'
modelHR = partial(model, domain=DOMAIN)
DOMAIN_DATA = 'Data/'
modelData = partial(model, domain=DOMAIN_DATA)
DOMAIN_TOOL = 'Tool/'
modelTool = partial(model, domain=DOMAIN_TOOL)