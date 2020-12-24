# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/progresses/management/commands/progresssummary.py
# Compiled at: 2018-11-14 13:10:17
from __future__ import unicode_literals
from django.db.models import Sum, Avg
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from aparnik.packages.educations.courses.models import Course, CourseSummary
from aparnik.packages.educations.progresses.models import Progresses, ProgressSummary
from aparnik.contrib.basemodels.models import BaseModel
import datetime
User = get_user_model()

class Command(BaseCommand):
    help = b'calculate for Progress Model'

    def handle(self, *args, **options):
        start_time = now()
        reindex = False
        if Progresses.objects.update_needed().count() > 0:
            reindex = True
        if reindex:
            self.reindex()
        Progresses.objects.update_needed().update(update_needed=False)
        finished_time = now()
        print b'reindex progress %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)

    def reindex(self):
        models = []
        for user_id in Progresses.objects.update_needed().values_list(b'user_obj', flat=True).distinct():
            user = User.objects.get(pk=user_id)
            progresses_user = Progresses.objects.this_user(user=user).prefetch_related(b'file_obj__course_obj__parent_obj')
            courses_ids = progresses_user.values_list(b'file_obj__course_obj', flat=True).distinct()
            parents = []
            for course_id in courses_ids:
                course = Course.objects.get(pk=course_id)
                if course.parent_obj:
                    parents.append(course.parent_obj)
                total_time_seconds = CourseSummary.objects.filter(course=course).aggregate(total_time_seconds=Sum(b'total_time_seconds'))[b'total_time_seconds'] or 0.0
                total_complete = progresses_user.filter(file_obj__course_obj=course).aggregate(total_time_seconds=Sum(b'file_obj__seconds'))[b'total_time_seconds'] or 0.0
                try:
                    percentage = total_complete / total_time_seconds * 100
                except:
                    percentage = 0.0

                try:
                    progress_summary = ProgressSummary.objects.get(user_obj=user, model=course)
                    progress_summary.percentage = percentage
                    progress_summary.save()
                except Exception as e:
                    ProgressSummary.objects.create(user_obj=user, model=course, percentage=percentage)

            while parents:
                parents_tmp = list(set(parents))
                parents = []
                for obj in parents_tmp:
                    if obj.parent_obj:
                        parents.append(obj.parent_obj)
                    percentage = ProgressSummary.objects.active().filter(user_obj=user, model__parent_obj=obj).aggregate(percentage_avg=Avg(b'percentage'))[b'percentage_avg'] or 0.0
                    try:
                        progress_summary = ProgressSummary.objects.get(user_obj=user, model=obj)
                        progress_summary.percentage = percentage
                        progress_summary.save()
                    except Exception as e:
                        ProgressSummary.objects.create(user_obj=user, model=obj, percentage=percentage)