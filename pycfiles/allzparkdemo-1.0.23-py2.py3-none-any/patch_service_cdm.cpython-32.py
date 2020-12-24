# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_mongrel2_server/patch_service_cdm.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 23, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the Mongrel2 web server plugins patch for the cdm.\n'
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