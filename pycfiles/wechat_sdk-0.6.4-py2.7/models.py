# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/context/framework/django/models.py
# Compiled at: 2014-12-20 23:11:43
from django.db import models

class ContextManager(models.Manager):

    def encode(self, openid, context_dict):
        return ContextStore(openid).encode(context_dict)

    def save(self, openid, context_dict, expire_date):
        s = self.model(openid, self.encode(openid, context_dict), expire_date)
        if context_dict:
            s.save()
        else:
            s.delete()
        return s


class Context(models.Model):
    openid = models.CharField('用户OpenID', max_length=50, primary_key=True)
    context_data = models.TextField('上下文对话数据')
    expire_date = models.DateTimeField('过期日期', db_index=True)
    objects = ContextManager()

    class Meta:
        db_table = 'wechat_context'
        verbose_name = '微信上下文对话'
        verbose_name_plural = '微信上下文对话'

    def get_decoded(self):
        return ContextStore(self.openid).decode(self.context_data)


from wechat_sdk.context.framework.django.backends.db import ContextStore