# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/mocha/mocha/signals.py
# Compiled at: 2017-05-13 11:01:57
from . import decorators as deco

@deco.emit_signal()
def upload_file(change):
    return change()


@deco.emit_signal()
def delete_file(change):
    return change()


@deco.emit_signal()
def send_mail(change, **kwargs):
    return change()