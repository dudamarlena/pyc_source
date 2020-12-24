# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_toolkit/kotti_toolkit/__init__.py
# Compiled at: 2018-09-19 00:15:46
"""
Created on 2017-12-14
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_toolkit')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_toolkit.kotti_configure

        to enable the ``kotti_toolkit`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_toolkit'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_toolkit:locale')
    config.add_renderer(name='csv', factory='kotti_toolkit.renderers.CSVRenderer')
    config.scan(__name__)