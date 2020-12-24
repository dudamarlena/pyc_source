# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jneight/workspace/django-mail-factory-extras/mailfactory_extras/__init__.py
# Compiled at: 2014-10-12 12:07:08


def get_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


VERSION = (0, 25)
__version__ = get_version()
__author__ = 'Javier Cordero'
__email__ = 'jcorderomartinez@gmail.com'
__license__ = 'Apache 2.0'
from .smsfactory import SMSFactory
smsfactory = SMSFactory()
try:
    from django.utils.module_loading import autodiscover_modules

    def autodiscover():
        autodiscover_modules('sms', register_to=smsfactory)


except ImportError:
    pass

default_app_config = 'mailfactory_extras.apps.MailFactoryExtrasConfig'