# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/test/test.py
# Compiled at: 2013-01-10 22:25:30
from crash_hound import CrashHound, ReportCrash, CommonChecks, SenderTropo

def check_fn():
    raise ReportCrash('42 is true!')


crash_sender = SenderTropo('YOUR TROPO.COM API KEY', '+56 ... YOUR MOBILE NUMBER ...')
crash_checker = CrashHound(crash_sender)
crash_checker.register_check('42 Checker', check_fn, notify_every=60)
crash_checker.register_check('Google.com Blah test', lambda : CommonChecks.website_check('http://google.com/blah'), notify_every=60)
crash_checker.run_checks(check_interval=10)