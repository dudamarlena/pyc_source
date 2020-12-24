# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/toyz/toyz/utils/security.py
# Compiled at: 2015-06-30 23:44:06


def encrypt_pickle(app_settings):
    """
    Encrypt the app settings using a config file. Not yet supported
    """
    raise ToyzError('Pickle encryption not yet supported')


def decrypt_pickle(app_settings, key):
    """
    Use the provided key to decrypt the config file. Not yet supported
    """
    raise ToyzError('Pickle encryption not yet supported')