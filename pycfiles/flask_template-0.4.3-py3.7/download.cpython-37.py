# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/proj/tasks/download.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 517 bytes
import requests
from proj.extensions import celery
from proj.utils.mail import send_task_status_email

@celery.task
def download_result(download_url, email):
    result_file = 'result_file.tar.gz'
    with requests.get(download_url, stream=True) as (r):
        r.raise_for_status()
        with open(result_file, 'wb') as (f):
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)

    send_task_status_email(status='download success', email=email)