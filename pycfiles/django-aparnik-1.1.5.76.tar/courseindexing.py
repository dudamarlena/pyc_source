# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/management/commands/courseindexing.py
# Compiled at: 2018-11-14 13:27:41
from __future__ import unicode_literals
from django.db.models import Sum
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from aparnik.packages.educations.courses.models import CourseFile, Course, CourseSummary, FileField
import datetime
User = get_user_model()

class Command(BaseCommand):
    help = b'calculate for index course'

    def handle(self, *args, **options):
        start_time = now()
        reindex = False
        if Course.objects.update_needed().count() > 0:
            reindex = True
        if CourseFile.objects.update_needed().count() > 0:
            reindex = True
        if reindex:
            self.reindex_course()
            from aparnik.packages.educations.progresses.models import Progresses
            Progresses.objects.all().update(update_needed=True)
        Course.objects.update_needed().update(update_needed=False)
        CourseFile.objects.update_needed().update(update_needed=False)
        finished_time = now()
        print b'reindex courses %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)

    def reindex_course(self):
        for course in Course.objects.active():
            courses_id = Course.objects.children_deep(course).values_list(b'id', flat=True).distinct()
            for type_tuple in FileField.FILE_TYPE:
                type = type_tuple[0]
                files = CourseFile.objects.get_this_type(type=type).filter(course_obj_id__in=courses_id)
                time = files.aggregate(total_time_seconds=Sum(b'seconds'))[b'total_time_seconds'] or 0.0
                total_times = course.total_times.filter(type=type)
                total_time = None
                is_save = False
                if total_times.count() == 0:
                    total_time = CourseSummary.objects.create(total_time_seconds=time, file_count=files.count(), file_count_preview=files.filter(is_free_field=True).count(), type=type, course=course)
                    total_time.save()
                    is_save = True
                else:
                    total_time = total_times.first()
                    old_total_seconds = total_time.total_time_seconds
                    if old_total_seconds != time.__str__() or total_time.file_count != files.count() or total_time.file_count_preview != files.filter(is_free_field=True).count():
                        total_time.total_time_seconds = time
                        total_time.file_count = files.count()
                        total_time.file_count_preview = files.filter(is_free_field=True).count()
                        total_time.save()
                        is_save = True
                if is_save:
                    course.save()

        return