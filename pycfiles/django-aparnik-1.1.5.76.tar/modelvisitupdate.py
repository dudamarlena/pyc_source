# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/counters/management/commands/modelvisitupdate.py
# Compiled at: 2019-02-10 08:55:09
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.db.models import Count, Subquery, OuterRef, F
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from aparnik.settings import aparnik_settings, Setting
from aparnik.contrib.counters.models import Counter
from aparnik.contrib.basemodels.models import BaseModel
UserSummeryListSerializer = aparnik_settings.USER_SUMMARY_LIST_SERIALIZER

class Command(BaseCommand):
    help = b'Updates visit counter for models based on a variable in settings app'

    def handle(self, *args, **options):
        start_time = now()
        try:
            is_count_per_view = Setting.objects.get(key=b'VISIT_COUNT_PER_VIEW').get_value()
        except:
            is_count_per_view = False

        if is_count_per_view:
            BaseModel.objects.update(visit_count=Coalesce(Subquery(BaseModel.objects.active().filter(counter__model_obj=OuterRef(b'id'), counter__action=b'v').annotate(count=Count(b'counter__create_date') or 0).values(b'count')), 0))
        if not is_count_per_view:
            BaseModel.objects.update(visit_count=Coalesce(Subquery(BaseModel.objects.active().filter(counter__model_obj=OuterRef(b'id'), counter__action=b'v').annotate(count=Count(b'counter__user_obj', distinct=True)).values(b'count')), 0))
            BaseModel.objects.update(visit_count=F(b'visit_count') + Coalesce(Subquery(BaseModel.objects.active().filter(counter__model_obj=OuterRef(b'id'), counter__user_obj_id__isnull=True, counter__action=b'v').annotate(count=Count(b'counter__user_obj', distinct=True)).values(b'count')), 0))
        finished_time = now()
        print b'counters updated %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)