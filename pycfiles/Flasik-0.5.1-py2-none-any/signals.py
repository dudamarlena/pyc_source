# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/signals.py
# Compiled at: 2019-08-24 19:04:01
from functions import emit_signal

@emit_signal()
def upload_file(change):
    return change()


@emit_signal()
def delete_file(change):
    return change()


@emit_signal()
def send_mail(change, **kwargs):
    return change()