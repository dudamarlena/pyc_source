# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rdisq/identification.py
# Compiled at: 2020-03-07 02:12:19
# Size of source mod 2**32: 323 bytes
__author__ = 'smackware'
import os, uuid

def get_mac():
    return uuid.getnode()


def get_consumer_id():
    return '%s-%s' % (get_mac(), os.getpid())


def get_request_key(task_id):
    return 'request_%s' % (task_id,)


def generate_task_id():
    return '%s-%s' % (get_consumer_id(), uuid.uuid4().hex)