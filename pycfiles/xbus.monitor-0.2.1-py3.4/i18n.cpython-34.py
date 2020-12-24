# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/i18n.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 507 bytes
"""Internationalization helpers."""
from pyramid.i18n import get_localizer, TranslationStringFactory
translation_factory = None

def init_i18n(config):
    global translation_factory
    translation_factory = TranslationStringFactory('xbus_monitor')
    config.add_translation_dirs('xbus.monitor:locale/')


def req_l10n(request):
    localizer = get_localizer(request)
    return lambda string: localizer.translate(translation_factory(string))