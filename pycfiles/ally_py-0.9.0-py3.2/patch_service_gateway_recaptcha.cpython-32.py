# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/captcha/patch_service_gateway_recaptcha.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 23, 2013

@package: captcha
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the reCAPTCHA gateway service setup patch.
"""
from ally.container import ioc
import logging
log = logging.getLogger(__name__)
try:
    from __setup__ import ally_gateway_recaptcha
    from __setup__ import ally_core_http
except ImportError:
    log.info('No reCAPTCHA gateway service available, thus no need to publish the captcha gateway URI')
else:
    from __setup__.ally_core_http.processor import root_uri_resources
    from __setup__.ally_gateway_recaptcha.processor import gateway_captcha_uri

    @ioc.replace(gateway_captcha_uri)
    def gateway_captcha_uri():
        """
        The captcha URI.
        """
        return root_uri_resources() % '/Gateway/Captcha'