# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/__init__.py
# Compiled at: 2018-09-19 02:38:20
"""
Created on 2018-09-19
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_group_manager')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_group_manager.kotti_configure

        to enable the ``kotti_group_manager`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_group_manager'
    settings['kotti.alembic_dirs'] += ' kotti_group_manager:alembic'
    settings['kotti.available_types'] += ' kotti_group_manager.resources.GroupPage'
    settings['kotti.fanstatic.view_needed'] += ' kotti_group_manager.fanstatic.css_and_js'
    settings['kotti.populators'] += ' kotti_group_manager.populator.populate'
    File.type_info.addable_to.append('GroupPage')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_group_manager:locale')
    config.add_static_view('static-kotti_group_manager', 'kotti_group_manager:static')
    config.add_route('find-group', '_group/{group}')
    config.scan(__name__)