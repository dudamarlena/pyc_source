# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_gsd/kotti_gsd/__init__.py
# Compiled at: 2017-05-31 18:07:10
"""
Created on 2017-05-11
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_gsd')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_gsd.kotti_configure

        to enable the ``kotti_gsd`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_gsd'
    settings['kotti.fanstatic.view_needed'] += ' kotti_gsd.fanstatic.css_and_js'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_gsd:locale')
    config.add_static_view('static-kotti_gsd', 'kotti_gsd:static')
    config.scan(__name__)