# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_mail/include.py
# Compiled at: 2020-02-20 09:58:33
# Size of source mod 2**32: 1133 bytes
"""PyAMS_mail.include module

This module is used for Pyramid integration
"""
from pyramid_mailer import IMailer, Mailer
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_mail:locales')
    config.scan()
    settings = config.registry.settings
    mailers = settings.get('pyams_mail.mailers')
    if mailers:
        for prefix in mailers.split():
            config.registry.registerUtility(Mailer.from_settings(settings, prefix), IMailer, name=settings['{0}name'.format(prefix)])