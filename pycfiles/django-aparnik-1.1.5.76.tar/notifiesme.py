# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifiesme/management/commands/notifiesme.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from aparnik.contrib.notifications.models import Notification
from aparnik.contrib.notifiesme.models import NotifyMe
from aparnik.contrib.basemodels.models import BaseModel
from aparnik.packages.educations.courses.models import Course, CourseFile
from aparnik.packages.shops.products.models import Product
import datetime
User = get_user_model()

class Command(BaseCommand):
    help = b'send notifies me'

    def handle(self, *args, **options):
        start_time = now()
        current_time = now()
        last_time = now() + relativedelta(minutes=-4)
        notifies_request_id = NotifyMe.objects.active().values_list(b'model_obj__id', flat=True).distinct()
        ids = []
        course_queryset = Course.objects.children_deep(course_ids=list(notifies_request_id))
        courses_ids = course_queryset.values_list(b'id', flat=True)
        courses_new_ids = []
        if course_queryset.filter(publish_date__range=[last_time, current_time]).exists():
            courses_new_ids = course_queryset.filter(publish_date__range=[last_time, current_time]).values_list(b'id', flat=True)
        file_queryset = CourseFile.objects.active().filter(course_obj_id__in=courses_ids, publish_date__range=[last_time, current_time])
        files_new_ids = []
        if file_queryset.exists():
            files_new_ids = file_queryset.values_list(b'id', flat=True)
        if len(files_new_ids) or len(courses_new_ids):
            self.reindex(notifies_request_id, courses_new_ids, files_new_ids)
        finished_time = now()
        print b'send notifies me %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)

    def reindex(self, notifies_request_id, courses_new_ids, files_new_ids):
        union_ids = list(courses_new_ids) + list(files_new_ids)
        for nid in union_ids:
            ids = []
            try:
                try:
                    ids.append(CourseFile.objects.get(id=nid).course_obj.id)
                except:
                    pass

            finally:
                ids.append(nid)

            ids = ids + list(Course.objects.parents_deep(course_id=ids[0]).values_list(b'id', flat=True).distinct())
            ids = list(set(ids))
            compare_ids = [ x for x in ids if x not in union_ids ]
            if not len(compare_ids) == len(ids):
                users_id = NotifyMe.objects.active().filter(model_obj_id__in=ids).order_by(b'user_obj').values_list(b'user_obj', flat=True).distinct()
                product = Product.objects.get(id=nid)
                try:
                    Notification.objects.send_notification(type=Notification.NOTIFICATION_INFO, users=User.objects.filter(pk__in=users_id), title=b'فایل جدید', description=b'%s در دسترس قرار گرفت.' % product.title, from_user_obj=None, model_obj=product)
                except Exception as e:
                    print e.message

        return