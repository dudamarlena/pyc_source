# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_decoy/__init__.py
# Compiled at: 2014-12-20 15:40:48
"""Main decoy module."""
import logging
__version__ = '0.1.0'
logger = logging.getLogger(__name__)
SETTINGS_PREFIX = 'decoy'

def includeme(configurator):
    """
    Configure decoy plugin on pyramid application.

    :param pyramid.configurator.Configurator configurator: pyramid's
        configurator object
    """
    configurator.registry['decoy'] = get_decoy_settings(configurator.get_settings())
    configurator.add_route('decoy', pattern='/*p')
    configurator.add_view('pyramid_decoy.views.decoy', route_name='decoy')


def get_decoy_settings(settings):
    """
    Extract decoy settings out of all.

    :param dict settings: pyramid app settings
    :returns: decoy settings
    :rtype: dict
    """
    return {k.split('.', 1)[(-1)]:v for k, v in settings.items() if k[:len(SETTINGS_PREFIX)] == SETTINGS_PREFIX if k[:len(SETTINGS_PREFIX)] == SETTINGS_PREFIX}