# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidsingleton/proj/pocket-cronv/venv/lib/python2.7/site-packages/simplescheduler/cli.py
# Compiled at: 2015-04-11 17:27:47
import argparse
from .scheduler import Job, Scheduler
from .version import VERSION
__version__ = VERSION
parser = argparse.ArgumentParser(description='SimpleScheduler\n    redis parameters will be read from environment variables:\n    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_KEY (password)    \n    ')
parser.add_argument('--interval', type=int, default=5, help='Interval in seconds between scheduler polls.')
parser.add_argument('--verbose', type=bool, default=False, help='Be more verbose.')
parser.add_argument('--keepalive', type=bool, default=False, help='Run a keepalive task.')

def main():
    """ SimpleScheduler
    redis parameters will be read from environment variables:
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_KEY (password)
    """
    args = parser.parse_args()
    scheduler = Scheduler()
    print 'Start %s' % scheduler.scheduler_id
    scheduler.interval = args.interval
    if args.keepalive:
        scheduler.run(once=True)
        keepalive = Job('simplescheduler.keepalive', args=[
         0,
         scheduler.get_running_scheduler_id(),
         args.interval * 2])
        scheduler.schedule(keepalive, long(time.time() * 1000000))
    scheduler._run()