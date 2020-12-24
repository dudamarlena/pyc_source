# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sms/base.py
# Compiled at: 2014-08-01 07:08:33
import os
from abc import ABCMeta, abstractmethod
from django.utils import six
from django.template import TemplateDoesNotExist
from mail_factory.mails import BaseMail

class BaseSMS(BaseMail, six.with_metaclass(ABCMeta)):

    def get_template_part(self, part, lang=None):
        templates = []
        localized = os.path.join('sms', self.template_name, lang or self.lang, part)
        templates.append(localized)
        fallback = os.path.join('sms', self.template_name, part)
        templates.append(fallback)
        return templates

    def mail_admins(self, attachments=None, from_email=None):
        raise NotImplementedError()

    def create_sms_msg(self, lang=None):
        try:
            body = self._render_part('body.txt', lang=lang)
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist('Txt template have not been found')

        return body

    @abstractmethod
    def send(self, to_phone, from_phone=None):
        pass