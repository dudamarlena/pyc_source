# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/indexing/patch_service_assemblage.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Jan 23, 2013

@package: assemblage
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the assemblage service setup patch.
"""
from ally.container import ioc
from ally.support.api.util_service import nameForModel
from indexing.api.domain_indexing import DOMAIN
from indexing.api.indexing import Block
import logging
log = logging.getLogger(__name__)
try:
    from __setup__ import ally_assemblage
    from __setup__ import ally_core_http
except ImportError:
    log.info('No assemblage service available, thus no need to publish the assemblage data')
else:
    from __setup__.ally_assemblage.processor import assemblage_indexes_uri
    from __setup__.ally_core_http.server import root_uri_resources

    @ioc.replace(assemblage_indexes_uri)
    def assemblage_indexes_uri_internal():
        """
        The assemblage indexes URI.
        """
        return ''.join((root_uri_resources(), '/', DOMAIN, nameForModel(Block), '/%s'))