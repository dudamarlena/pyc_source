# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/cdm/patch_mongrel2_server.py
# Compiled at: 2013-10-23 08:37:55
"""
Created on Nov 23, 2011

@package: support cdm
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the Mongrel2 web server plugins patch for the cdm.
"""
from __setup__.ally_http.server import server_type
from ally.container import ioc, support
from ..cdm.service import use_linked_cdm
ioc.doc(use_linked_cdm, '\n!!!Attention, if the mongrel2 server is selected this option will always be "false"\n')

@ioc.before(use_linked_cdm, auto=False)
def use_linked_cdm_force():
    if server_type() == 'mongrel2':
        support.force(use_linked_cdm, False)