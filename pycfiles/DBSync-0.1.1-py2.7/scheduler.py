# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dbsync/scheduler.py
# Compiled at: 2015-04-10 05:21:53
__author__ = 'nathan'
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time
jobstores = {'default': MemoryJobStore()}
executors = {'default': ThreadPoolExecutor(20), 
   'processpool': ProcessPoolExecutor(5)}
job_defaults = {'coalesce': False, 
   'max_instances': 3}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

def say_hello(name):
    print 'Hello ' + name


scheduler.add_job(say_hello, 'interval', ['Bangtao'], seconds=2)
scheduler.add_job(say_hello, 'interval', ['Baixue'], seconds=2)
scheduler.start()
print scheduler.get_jobs()
scheduler.print_jobs()
while True:
    time.sleep(5)