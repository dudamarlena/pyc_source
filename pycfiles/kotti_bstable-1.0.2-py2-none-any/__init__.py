# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/environment/dpisonline/src/kotti_bstable/kotti_bstable/__init__.py
# Compiled at: 2020-03-23 23:35:38
"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_bstable')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_bstable.kotti_configure

        to enable the ``kotti_bstable`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_bstable'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_bstable:locale')
    config.add_static_view('static-kotti_bstable', 'kotti_bstable:static')
    config.scan(__name__)