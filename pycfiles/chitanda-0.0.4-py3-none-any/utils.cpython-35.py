# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/common/utils.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 4375 bytes
from __future__ import print_function
from __future__ import division
from past.utils import old_div
import datetime, pytz
from tzlocal import get_localzone
from chisubmit.repos.factory import RemoteRepositoryConnectionFactory
import math
from datetime import timedelta
localzone = get_localzone()
now_override = None

def get_datetime_now_utc():
    global now_override
    if now_override is None:
        return datetime.datetime.now(pytz.utc).replace(microsecond=0)
    else:
        return now_override


def set_testing_now(dt):
    global now_override
    now_override = dt


def set_datetime_timezone_utc(dt):
    return pytz.utc.localize(dt)


def convert_datetime_to_utc(dt, default_tz=localzone):
    if dt.tzinfo is None:
        dt = localzone.localize(dt)
    return dt.astimezone(pytz.utc)


def convert_datetime_to_local(dt, default_tz=localzone):
    if dt.tzinfo is None:
        dt = localzone.localize(dt)
    return dt.astimezone(localzone)


def parse_timedelta(s):
    l = s.split(':')
    l = [int(x) for x in l]
    if len(l) == 2:
        return datetime.timedelta(hours=l[0], minutes=l[1])
    if len(l) == 3:
        return datetime.timedelta(hours=l[0], minutes=l[1], seconds=l[2])
    raise ValueError('Incorrectly formatted timedelta: %s' % s)


def compute_extensions_needed(submission_time, deadline):
    delta = (submission_time - deadline).total_seconds()
    extensions_needed = math.ceil(old_div(delta, 86400.0))
    if extensions_needed <= 0:
        return 0
    else:
        return int(extensions_needed)


def is_submission_ready_for_grading(assignment_deadline, submission_date, extensions_used, assignment_grace_period=datetime.timedelta(0)):
    now = get_datetime_now_utc()
    deadline = assignment_deadline + assignment_grace_period + timedelta(days=extensions_used)
    if now > deadline:
        return True
    else:
        return False


def create_connection(course, config, staging=False):
    if not staging:
        connstr = course.git_server_connstr
    else:
        connstr = course.git_staging_connstr
    if connstr is None:
        print("The course's git server has not been configured.")
        print('Please contact the course instructor or the chisubmit administrator.')
        return
    else:
        ssl_verify = config.get_ssl_verify()
        conn = RemoteRepositoryConnectionFactory.create_connection(connstr, staging, ssl_verify)
        server_type = conn.get_server_type_name()
        git_credentials = config.get_git_credentials(server_type)
        if git_credentials is None:
            print('You do not have %s credentials.' % server_type)
            return
        conn.connect(git_credentials)
        return conn