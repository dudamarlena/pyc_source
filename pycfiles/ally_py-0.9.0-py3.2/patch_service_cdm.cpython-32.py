# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_mongrel2_server/patch_service_cdm.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Nov 23, 2011

@package: ally http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the Mongrel2 web server plugins patch for the cdm.
"""
from ..ally_http import server_type
from ally.container import ioc, support
import logging
log = logging.getLogger(__name__)
try:
    from .. import ally_cdm
except ImportError:
    log.info('No local CDM service to stop from delivering content')
else:
    ally_cdm = ally_cdm
    from ..ally_cdm.server import server_provide_content
    ioc.doc(server_provide_content, '\n    !Attention, if the mongrel2 server is selected this option will always be "false"\n    ')

    @ioc.before(server_provide_content, auto=False)
    def server_provide_content_force():
        if server_type() == 'mongrel2':
            support.force(server_provide_content, False)