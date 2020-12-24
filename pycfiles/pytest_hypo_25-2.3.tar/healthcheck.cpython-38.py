# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\healthcheck.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1310 bytes
from hypothesis.errors import FailedHealthCheck

def fail_health_check(settings, message, label):
    __tracebackhide__ = True
    if label in settings.suppress_health_check:
        return
    message += '\nSee https://hypothesis.readthedocs.io/en/latest/healthchecks.html for more information about this. If you want to disable just this health check, add %s to the suppress_health_check settings for this test.' % (
     label,)
    raise FailedHealthCheck(message, label)