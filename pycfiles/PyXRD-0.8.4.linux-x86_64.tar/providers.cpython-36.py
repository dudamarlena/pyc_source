# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/providers.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1308 bytes
import logging
logger = logging.getLogger(__name__)
from pyxrd.data.settings import ASYNC_SERER_PROVIDERS, ASYNC_SERVER_PRELOAD
_async_provider = None

def load_provider():
    global _async_provider
    logger.info('Loading async server provider')
    for class_path in ASYNC_SERER_PROVIDERS:
        logger.info('Trying to load async server provider at %s' % class_path)
        try:
            components = class_path.split('.')
            class_name = components[(-1)]
            mod = __import__(('.'.join(components[:-1])), fromlist=[class_name])
            klass = getattr(mod, class_name)
        except (ImportError, AttributeError):
            logger.warning('Failed to import async provider %s!' % class_path)
            continue

        _async_provider = klass
        break

    logger.info("Loaded async server provider '%s'" % _async_provider)


if ASYNC_SERVER_PRELOAD:
    load_provider()
    if _async_provider is not None:
        _async_provider.launch_server()

def get_provider():
    if _async_provider is None:
        load_provider()
    return _async_provider


def get_status():
    return get_provider().get_status()