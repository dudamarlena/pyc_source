# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/common_dibbs/clients/rpa_client/configure.py
# Compiled at: 2016-08-15 14:43:05


def configure_auth(value, prefix='Token', label='Authorization'):
    import configuration
    config = configuration.Configuration()
    config.api_key_prefix.update({label: prefix})
    config.api_key.update({label: value})


def configure_auth_basic(username, password):
    from apis.users_api import UsersApi
    credentials = {'username': username, 'password': password}
    ret = UsersApi().api_token_auth_post(data=credentials)
    token = ret.token
    configure_auth(token)


def configure_host(value):
    import configuration
    config = configuration.Configuration()
    config.host = value