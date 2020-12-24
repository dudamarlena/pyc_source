# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/passwordless/login_url.py
# Compiled at: 2017-11-22 16:02:35
import abc

class LoginURL(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        pass

    @abc.abstractmethod
    def generate(self, token, userid):
        pass

    @abc.abstractmethod
    def parse(self, request):
        pass


class PlainLoginURL(LoginURL):

    def generate(self, token, userid):
        from flask import url_for
        return ('').join([
         url_for('authenticate', _external=True),
         ('?token={0}&uid={1}').format(token, userid)])

    def parse(self, request):
        token = request.values['token']
        uid = request.values['uid']
        return (token, uid)


LOGIN_URLS = {'plain': PlainLoginURL}