# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_restful_api/kotti_restful_api/__init__.py
# Compiled at: 2016-12-20 13:28:29
"""
Created on 2016-12-20
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.i18n import TranslationStringFactory
from kotti_restful_api import requests
_ = TranslationStringFactory('kotti_restful_api')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_restful_api.kotti_configure

        to enable the ``kotti_restful_api`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_restful_api'
    settings['kotti.alembic_dirs'] += ' kotti_restful_api:alembic'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_restful_api:locale')
    config.add_view_predicate('content_type', requests.ContentTypePredicate)
    config.add_view_predicate('cross_request', requests.CrossRequestPredicate)
    config.scan(__name__)