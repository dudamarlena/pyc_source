# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_survey/kotti_survey/__init__.py
# Compiled at: 2016-06-17 05:39:38
"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_survey')

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_survey.kotti_configure

        to enable the ``kotti_survey`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    settings['pyramid.includes'] += ' kotti_survey'
    settings['kotti.alembic_dirs'] += ' kotti_survey:alembic'
    settings['kotti.available_types'] += ' kotti_survey.resources.Survey kotti_survey.resources.Question kotti_survey.resources.AnswerField'
    settings['kotti.fanstatic.view_needed'] += ' kotti_survey.fanstatic.css_and_js'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_translation_dirs('kotti_survey:locale')
    config.add_static_view('static-kotti_survey', 'kotti_survey:static')
    config.scan(__name__)