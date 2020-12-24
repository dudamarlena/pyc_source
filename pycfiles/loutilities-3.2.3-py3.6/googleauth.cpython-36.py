# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\googleauth.py
# Compiled at: 2019-11-27 06:58:31
# Size of source mod 2**32: 7331 bytes
import os.path
from flask import jsonify, url_for, session, request, abort
from flask.views import View
import httplib2
from oauth2client import client
from oauth2client.file import Storage

class GoogleAuth(View):

    def __init__(self, app, client_secrets_file, scopes, startendpoint, credfolder=None, logincallback=lambda email: None, logoutcallback=lambda email: None, loginfo=None, logdebug=None, logerror=None):
        """
        :param app: flask application
        :param client_secrets_file: client_secrets.json path
        :param scopes: list of google scopes. see https://developers.google.com/identity/protocols/googlescopes
        :param startendpoint: endpoint to start with after authorization completed (no leading slash)
        :param credfolder: folder where credential Storage will be placed
        :param logincallback: function(email) called when login detected
        :param logoutcallback: function called when logout detected
        :param loginfo: info logger function
        :param logdebug: debug logger function
        :param logerror: debug logger function
        """
        self.app = app
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.startendpoint = startendpoint
        self.credfolder = credfolder
        self.logincallback = logincallback
        self.logoutcallback = logoutcallback
        self.loginfo = loginfo
        self.logdebug = logdebug
        self.logerror = logerror
        self.app.add_url_rule('/_token', view_func=(self.token), methods=['POST'])
        self.app.add_url_rule('/clear', view_func=(self.clear_credentials), methods=['GET'])

    def token(self):
        auth_code = request.data
        if not request.headers.get('X-Requested-With'):
            abort(403)
        credentials = client.credentials_from_clientsecrets_and_code(self.client_secrets_file, self.scopes, auth_code)
        user_id = credentials.id_token['sub']
        email = credentials.id_token['email']
        authorized = False
        if user_id:
            credfile = os.path.join(self.credfolder, user_id)
            storage = Storage(credfile)
            storedcred = storage.get()
            if not credentials.refresh_token:
                if storedcred:
                    storedcred.access_token = credentials.access_token
                    storedcred.token_expiry = credentials.token_expiry
                    credentials = storedcred
            credentials.set_store(storage)
            storage.put(credentials)
            session['_ga_google_user_id'] = user_id
            session['_ga_google_email'] = email
            http = httplib2.Http()
            credentials.refresh(http)
            authorized = self.logincallback(email)
        if self.logdebug:
            self.logdebug('oauth2callback() session = {}'.format(session))
        return jsonify({'authorized':authorized,  'redirect':url_for(self.startendpoint)})

    def clear_credentials(self):
        if 'credentials' in session:
            del session['credentials']
        else:
            if '_ga_google_user_id' in session:
                del session['_ga_google_user_id']
            email = None
            if '_ga_google_email' in session:
                email = session['_ga_google_email']
                del session['_ga_google_email']
        self.logoutcallback(email)
        return 'Credentials have been cleared from session cookie'

    def get_userid(self, credentials):
        try:
            user_id = session['_ga_google_user_id']
            if self.logdebug:
                self.logdebug('get_userid() retrieved user_id from session cookie')
        except KeyError:
            try:
                user_id = credentials.id_token['sub']
                if self.logdebug:
                    self.logdebug('get_userid() profile from credentials = {}'.format(credentials))
            except:
                if self.logdebug:
                    self.logdebug('invalid credentials, continuing')
                user_id = None

        return user_id


def get_credentials(credfolder):
    try:
        user_id = session['_ga_google_user_id']
        credfile = os.path.join(credfolder, user_id)
        storage = Storage(credfile)
        credentials = storage.get()
        credentials.set_store(storage)
    except KeyError:
        credentials = None

    return credentials


def get_email():
    try:
        email = session['_ga_google_email']
    except KeyError:
        email = None

    return email