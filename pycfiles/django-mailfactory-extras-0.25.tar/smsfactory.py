# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jneight/workspace/django-mail-factory-extras/mailfactory_extras/smsfactory.py
# Compiled at: 2014-08-04 07:00:00
""":synopsis: Just a simple version of the original Factory object but using SMS

"""
from mail_factory import exceptions

class SMSFactory(object):

    def __init__(self, *args, **kwargs):
        self.sms_map = {}

    def register(self, sms_klass):
        if not hasattr(sms_klass, 'template_name'):
            raise exceptions.MailFactoryError(('{0} needs a template_name parameter to be registered').format(sms_klass.__name__))
        self.sms_map[sms_klass.template_name] = sms_klass

    def unregister(self, sms_klass):
        if not hasattr(sms_klass, 'template_name'):
            raise exceptions.MailFactoryError(('{0} needs a template_name parameter to be registered').format(sms_klass.__name__))
        del sms_klass[sms_klass.template_name]

    def send(self, template_name, to_phone, context):
        return self.sms_map[template_name](context=context).send(to_phone)