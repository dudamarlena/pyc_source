# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/support_php.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jul 3, 2011

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides additional configurations for the Zend PHP client.
"""
from ..ally_core.encoder_decoder import content_types_json
from ally.container import ioc

@ioc.config
def php_zend_support() -> bool:
    """Provides additional configurations for the Zend PHP client"""
    return False


@ioc.before(content_types_json)
def updateContentTypesJSON():
    if php_zend_support():
        content_types_json()['application/x-www-form-urlencoded'] = 'application/x-www-form-urlencoded'