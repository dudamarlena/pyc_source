# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/environment/dpisonline/src/kotti_alert/kotti_alert/__init__.py
# Compiled at: 2019-09-18 14:40:37
"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.views.slots import assign_slot
from kotti.util import Link
from pyramid.i18n import TranslationStringFactory
from kotti_controlpanel import CONTROL_PANEL_LINKS
_ = TranslationStringFactory('kotti_alert')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_alert.kotti_configure

        to enable the ``kotti_alert`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_alert'
    settings['kotti.alembic_dirs'] += ' kotti_alert:alembic'
    settings['kotti.available_types'] += ' kotti_alert.resources.Alert'
    settings['kotti.fanstatic.view_needed'] += ' kotti_alert.fanstatic.css_and_js'
    assign_slot('kotti-alert', 'abovecontent')
    CONTROL_PANEL_LINKS.append(Link('all-alerts', title=_('Alerts')))


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_alert:locale')
    config.add_static_view('static-kotti_alert', 'kotti_alert:static')
    config.scan(__name__)