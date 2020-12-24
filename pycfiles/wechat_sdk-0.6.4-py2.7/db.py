# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/context/framework/django/backends/db.py
# Compiled at: 2014-12-20 23:11:43
from django.db import IntegrityError, transaction, router
from django.utils import timezone
from wechat_sdk.context.framework.django.backends.base import ContextBase, CreateError
from wechat_sdk.context.framework.django.exceptions import SuspiciousOpenID

class ContextStore(ContextBase):
    """
    数据库存储微信上下文对话
    """

    def __init__(self, openid):
        super(ContextStore, self).__init__(openid)

    def load(self):
        try:
            s = Context.objects.get(openid=self.openid, expire_date__gt=timezone.now())
            return self.decode(s.context_data)
        except (Context.DoesNotExist, SuspiciousOpenID) as e:
            self.create(self.openid)
            return {}

    def exists(self, openid):
        return Context.objects.filter(openid=openid).exists()

    def create(self, openid):
        self.save(must_create=True)
        self.modified = True
        self._session_cache = {}

    def save(self, must_create=False):
        obj = Context(openid=self.openid, context_data=self.encode(self._get_context(no_load=must_create)), expire_date=self.get_expiry_date())
        self.clear_expired()
        using = router.db_for_write(Context, instance=obj)
        try:
            with transaction.atomic(using=using):
                obj.save(force_insert=must_create, using=using)
        except IntegrityError:
            if must_create:
                raise CreateError
            raise

    def delete(self, openid=None):
        if openid is None:
            openid = self.openid
        try:
            Context.objects.get(openid=openid).delete()
        except Context.DoesNotExist:
            pass

        return

    @staticmethod
    def clear_expired():
        Context.objects.filter(expire_date__lt=timezone.now()).delete()


from wechat_sdk.context.framework.django.models import Context