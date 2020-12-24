# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/__init__.py
# Compiled at: 2017-06-09 03:03:53
"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.i18n import TranslationStringFactory
from kotti.util import Link
from kotti.views.site_setup import CONTROL_PANEL_LINKS as KOTTI_CP_LINKS
_ = TranslationStringFactory('kotti_controlpanel')
CONTROL_PANEL_LINKS = [
 Link('setup-users', 'User Management')]

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_controlpanel.kotti_configure

        to enable the ``kotti_controlpanel`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_controlpanel'
    settings['kotti.alembic_dirs'] += ' kotti_controlpanel:alembic'
    settings['kotti.fanstatic.view_needed'] += ' kotti_controlpanel.fanstatic.css_and_js'
    cp = Link('controlpanel', title=_('Control Panel'))
    KOTTI_CP_LINKS.append(cp)


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_controlpanel:locale')
    config.add_static_view('static-kotti_controlpanel', 'kotti_controlpanel:static')
    config.scan(__name__)