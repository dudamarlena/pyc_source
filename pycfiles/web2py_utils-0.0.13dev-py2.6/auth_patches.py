# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web2py_utils/auth_patches.py
# Compiled at: 2010-05-22 13:48:28


def set_controller(auth, controller='default', function='user'):
    auth.settings.controller = controller
    auth.settings.login_url = auth.url(function, args='login')
    auth.settings.logged_url = auth.url(function, args='profile')
    auth.settings.download_url = auth.url('download')
    auth.settings.login_next = auth.url('index')
    auth.settings.logout_next = auth.url('index')
    auth.settings.register_next = auth.url('index')
    auth.settings.verify_email_next = auth.url(function, args='login')
    auth.settings.profile_next = auth.url('index')
    auth.settings.retrieve_username_next = auth.url('index')
    auth.settings.retrieve_password_next = auth.url('index')
    auth.settings.request_reset_password_next = auth.url(function, args='login')
    auth.settings.reset_password_next = auth.url(function, args='login')
    auth.settings.change_password_next = auth.url('index')
    auth.settings.on_failed_authorization = auth.url(function, args='not_authorized')