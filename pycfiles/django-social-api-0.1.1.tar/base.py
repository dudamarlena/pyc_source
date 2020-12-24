# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-social-api/social_api/storages/base.py
# Compiled at: 2016-02-10 18:07:26
import logging
from abc import ABCMeta, abstractmethod, abstractproperty
from django.conf import settings

class TokensStorageAbstractBase(object):
    __metaclass__ = ABCMeta
    only_this = False

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def get_tokens(self):
        pass

    @abstractmethod
    def update_tokens(self):
        pass

    @abstractmethod
    def refresh_tokens(self):
        pass

    def __init__(self, provider, *args, **kwargs):
        self.provider = provider
        self.logger = self.get_logger()

    def get_from_context(self, name):
        key = ('_').join([self.name, name])
        context = getattr(settings, 'SOCIAL_API_CALL_CONTEXT', None)
        if context and self.provider in context and key in context[self.provider]:
            return context[self.provider][key]
        else:
            return

    def get_logger(self):
        return logging.getLogger('%s_api' % self.provider)