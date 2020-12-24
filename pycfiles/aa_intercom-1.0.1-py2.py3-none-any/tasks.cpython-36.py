# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./../aa_airtable/tasks.py
# Compiled at: 2017-06-21 22:01:48
# Size of source mod 2**32: 1723 bytes
import sys, traceback
from importlib import import_module
from django.conf import settings
from django.core.cache import cache
from aa_airtable.download import get
LOCK_EXPIRE = 300
from aa_airtable.celery import app

@app.task(ignore_result=True)
def process_job_task(job_id):
    from aa_airtable.parser import DatabasesParser
    from aa_airtable.models import Job
    lock_id = 'airtable-job-{}'.format(job_id)
    acquire_lock = lambda : cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda : cache.delete(lock_id)
    job = Job.objects.get(id=job_id)
    job.status = Job.STATUS_PRE_LOCK
    job.save()
    if acquire_lock():
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            release_lock()
            raise

        print('x3')
        job.status = Job.STATUS_STARTED
        job.save()
        print('x4')
        try:
            file_path, data = get()
            print('x5')
            job.file = file_path
            print('6')
            job.save()
            print(1)
            DatabasesParser(data)
            print(2)
            job.status = Job.STATUS_SUCCESS
            job.save()
            release_lock()
        except Exception as e:
            job.status = Job.STATUS_ERROR
            exc_type, exc_value, exc_traceback = sys.exc_info()
            job.error = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
            job.save()
            release_lock()
            raise e