# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/management/commands/filemultiqualities.py
# Compiled at: 2019-07-20 07:43:37
# Size of source mod 2**32: 1807 bytes
from django.core.management import BaseCommand
from django.utils.timezone import now
import dateutil.relativedelta as relativedelta
import subprocess, os
from aparnik.contrib.filefields.models import FileField

class Command(BaseCommand):
    help = 'Generate multiple qualities File fields'

    def handle(self, *args, **options):
        start_time = now()
        queryset = FileField.objects.multi_quality()
        for file in queryset:
            path = file.file_direct.path
            infile = path
            outfile = '%s%s' % (path, file.file_another_quality)
            if file.type == FileField.FILE_MOVIE:
                file.multi_quality_processing = 1
                if file.is_lock:
                    is_lock = file.is_lock
                    file.is_lock = not is_lock
                    file.save()
                    file.is_lock = is_lock
                subprocess.call(("ffmpeg -i '%s' -preset slow -b:a 128k -codec:v libx265 -pix_fmt yuv420p -b:v 750k -minrate 400k -maxrate 1000k -bufsize 1500k -vf scale=-1:360 '%s'" % (path, outfile)), shell=True, close_fds=True)
            file.multi_quality_processing = 2
            if file.is_lock:
                is_lock = file.is_lock
                file.is_lock = not is_lock
                file.save()
                file.is_lock = is_lock
            file.save()

        finished_time = now()
        print('multiple qualities done %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds))