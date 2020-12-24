# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/googleauthentication/browser/session_token.py
# Compiled at: 2010-03-24 18:49:57
__author__ = "D'Elia Federica"
from Products.Five.browser import BrowserView
from gdata.auth import AuthSubToken
from gdata.docs.service import DocsService
from gdata.auth import generate_auth_sub_url

class SessionToken(BrowserView):
    __module__ = __name__

    def convert_to_a_session_token(self, sigle_token):
        scope = [
         'http://docs.google.com/feeds/', 'http://spreadsheets.google.com/feeds/']
        authsub_token = AuthSubToken(scopes=scope)
        authsub_token.set_token_string(sigle_token)
        gd_client = DocsService()
        gd_client.auth_token = authsub_token
        gd_client.UpgradeToSessionToken(token=authsub_token)
        session_token = gd_client.auth_token.get_token_string()
        return session_token

    def get_auth_sub_url(self, came_from):
        porturl = self.context.portal_url()
        if came_from == None:
            next = porturl + '/logged_in'
        else:
            next = porturl + '/logged_in?came_from=' + came_from
        scope = ['http://docs.google.com/feeds/', 'http://spreadsheets.google.com/feeds/']
        secure = False
        session = True
        gd_client = DocsService()
        return generate_auth_sub_url(next, scope, secure, session)