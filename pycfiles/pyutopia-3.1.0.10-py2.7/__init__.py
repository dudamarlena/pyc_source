# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/__init__.py
# Compiled at: 2017-06-20 22:43:55
from utopia.log import logger
try:
    import utopiabridge as bridge
    bridge.proxyUrllib2()
    import utopiaauth as auth
except (AttributeError, ImportError):
    import sys
    logger.debug('Could not find package utopiabridge:', exc_info=True)
    logger.info('This script does not seem to be running inside Utopia Documents. Some functions will not work.')
    bridge = None
    auth = None

import utopia.extension

class Configurator(utopia.extension.Extension):
    pass


class Cancellation(RuntimeError):
    """The user has cancelled this task."""
    pass


def get_plugin_data(path):
    try:
        import inspect, sys
        loader = None
        for frame in inspect.stack():
            loader = frame[0].f_globals.get('__loader__')
            if loader is None:
                plugin_name = frame[0].f_globals.get('__plugin__', None)
                if plugin_name is not None:
                    loader = getattr(sys.modules.get(plugin_name), '__loader__', None)
            if loader is not None:
                break

        if loader is not None:
            return loader.get_data(path)
    except:
        logger.error('Could not fetch plugin data %s', path, exc_info=True)

    return


def get_plugin_data_as_url(path, mime):
    try:
        data = get_plugin_data(path)
        if data is not None:
            import base64
            encoded = base64.standard_b64encode(data)
            return ('data:{0};base64,{1}').format(mime, encoded)
    except:
        logger.error('Could not fetch plugin data %s', path, exc_info=True)

    return


import os
try:
    import utopia.plugins
    for package_path in utopia.plugins.__path__:
        for plugins_path in os.listdir(package_path):
            plugins_path = os.path.join(package_path, plugins_path)
            if os.path.isdir(plugins_path):
                utopia.extension.loadPlugins(plugins_path)

except:
    logger.debug('utopia.plugins could not be imported', exc_info=True)
    logger.info('No plugins installed, so functionality will be minimal.')

if 'UTOPIA_PLUGIN_PATH' in os.environ:
    for path in os.environ.get('UTOPIA_PLUGIN_PATH', '').split(os.pathsep):
        utopia.extension.loadPlugins(path.strip())

__all__ = [
 'bridge',
 'auth',
 'Configurator',
 'Cancellation',
 'get_plugin_data',
 'get_plugin_data_as_url']