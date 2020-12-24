# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/reporter/aspects.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 493 bytes


class Aspects:
    lock_request_count = 'lock_request_count'
    lock_acquire_count = 'lock_acquire_count'
    lock_release_count = 'lock_release_count'
    lock_release_wait = 'lock_release_wait'
    lock_acquire_wait = 'lock_acquire_wait'
    lock_acquire_fail_count = 'lock_acquire_fail_count'

    @staticmethod
    def validate(*aspects):
        for aspect in aspects:
            if not hasattr(Aspects, aspect):
                raise ValueError(f"aspect {repr(aspect)} not supported")