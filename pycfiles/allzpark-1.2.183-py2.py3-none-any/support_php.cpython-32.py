# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/support_php.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jul 3, 2011\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides additional configurations for the Zend PHP client.\n'
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