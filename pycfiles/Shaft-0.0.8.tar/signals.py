# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/contrib/auth/signals.py
# Compiled at: 2017-02-07 04:25:56
from shaft.decorators import emit_signal
from blinker import Namespace
ns = Namespace()

@emit_signal(namespace=ns)
def on_register(cb):
    """
    Emit a signal when signing up
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_login(cb):
    """
    Emit signal when logged in
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_logout(cb):
    """
    :param cb: callback function to execute
    :return: Current user
    """
    return cb()


@emit_signal(namespace=ns)
def on_info_updated(cb):
    """
    :param cb: callback function to execute
    :return:
    """
    return cb()


@emit_signal(namespace=ns)
def on_login_changed(cb):
    """
    :param cb: callback function to execute
    :return: the email that was changed
    """
    return cb()


@emit_signal(namespace=ns)
def on_password_changed(cb):
    """
    :param cb: callback function to execute
    :return: the password changed
    """
    return cb()


@emit_signal(namespace=ns)
def on_email_verified(cb):
    """
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_password_reset(cb):
    """
    :param cb: callback function to execute
    :return: The new password
    """
    return cb()


@emit_signal(namespace=ns)
def on_email_confirmed(cb):
    """
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()