# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_seatbelt/allow_callbacks.py
# Compiled at: 2011-07-05 10:31:28


def allow_usr_lib(path):
    """
    White-list helper that allows anything installed in /usr/lib/
    """
    return path.startswith('/usr/lib/')


DEFAULT_ALLOW_CALLBACKS = [
 allow_usr_lib]