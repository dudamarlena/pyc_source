# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
        return (
         token, uid)


LOGIN_URLS = {'plain': PlainLoginURL}