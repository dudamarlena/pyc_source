# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/email.py
# Compiled at: 2013-07-30 09:02:45
"""
E-Mail functionality.
"""
import subprocess

def compose():
    raise NotImplementedError()


def send():
    raise NotImplementedError()


def xdg_compose(to, subject, body=None, cc=None, bcc=None):
    """Use xdg-email to compose in an X environment.

    Needs xdg-utils and a running X session. Works with GNOME, KDE,
    MATE, XFCE, ...
    """
    command = [
     'xdg-email', '--utf8', '--subject', subject]
    if body:
        command += ['--body', body]
    if cc:
        if type(cc) is list:
            cc = (', ').join(cc)
        command += ['--cc', cc]
    if bcc:
        if type(bcc) is list:
            bcc = (', ').join(bcc)
        command += ['--bcc', bcc]
    if type(to) is list:
        to = (', ').join(to)
    command.append(to)
    return subprocess.call(command)