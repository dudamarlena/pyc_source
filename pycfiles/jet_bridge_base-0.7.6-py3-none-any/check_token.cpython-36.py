# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/commands/check_token.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 1045 bytes
import webbrowser
from requests import RequestException
from jet_bridge_base import settings
from jet_bridge_base.utils.backend import is_token_activated
from jet_bridge_base.logger import logger

def check_token_command(api_url):
    try:
        if not is_token_activated():
            logger.warning('[!] Your server token is not activated')
            logger.warning('[!] Token: {}'.format(settings.TOKEN))
            if settings.AUTO_OPEN_REGISTER and api_url.startswith('http'):
                register_url = '{}register/?token={}'.format(api_url, settings.TOKEN)
                if webbrowser.open(register_url):
                    logger.warning('[!] Activation page was opened in your browser - {}'.format(register_url))
            else:
                register_url = '{}register/'.format(api_url)
                logger.warning('[!] Go to {} to activate it'.format(register_url))
    except RequestException:
        logger.error("[!] Can't connect to Jet Admin API")
        logger.error('[!] Token verification failed')