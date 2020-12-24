# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/subscriptions/management/commands/subscriptions_management.py
# Compiled at: 2019-04-30 05:23:45
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.renderers import JSONRenderer
from dateutil.relativedelta import relativedelta
from aparnik.settings import aparnik_settings
from aparnik.contrib.notifications.models import Notification
from aparnik.packages.shops.subscriptions.models import SubscriptionOrder
json = JSONRenderer()
User = get_user_model()
UserSummeryListSerializer = aparnik_settings.USER_SUMMARY_LIST_SERIALIZER

class Command(BaseCommand):
    help = b'check subscription'

    def handle(self, *args, **options):
        start_time = now()
        one_week = now() + relativedelta(weeks=1)
        next_day = one_week + relativedelta(days=1)
        subscription_orders = SubscriptionOrder.objects.active().filter(expire_at__range=[one_week, next_day])
        self.send_notification(subscription_orders, 7)
        one_day = now()
        next_day = one_day + relativedelta(days=1)
        subscription_orders = SubscriptionOrder.objects.active().filter(expire_at__range=[one_day, next_day])
        self.send_notification(subscription_orders, 1)
        finished_time = now()
        print b'send Subscription %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)

    def send_notification(self, queryset, days_remain):
        if queryset.count() == 0:
            return
        Notification.objects.send_notification(User.objects.active().filter(pk__in=queryset.values_list(b'order_obj__user', flat=True).distinct()), type=Notification.NOTIFICATION_INFO, title=b'اکانت وی آي پی شما %s روز دیگر منقضی می شود' % days_remain, description=b'لطفا برای استفاده از خدمات ویژه ما اکانت خود را تمدید نمایید.')