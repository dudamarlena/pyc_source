# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/signals.py
# Compiled at: 2019-10-27 00:59:30
# Size of source mod 2**32: 252 bytes
from .functions import emit_signal

@emit_signal()
def upload_file(change):
    return change()


@emit_signal()
def delete_file(change):
    return change()


@emit_signal()
def send_mail(change, **kwargs):
    return change()