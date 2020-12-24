# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/services/service.py
# Compiled at: 2017-02-01 10:41:14
import os.path, requests, sys
BASE_URL = 'https://socialize.dmonn.ch/api/'

class Service(object):

    def get(self, path):
        home_directory = os.path.expanduser('~')
        authtoken_file = os.path.join(home_directory, '.AUTHTOKEN')
        if os.path.isfile(authtoken_file):
            try:
                token = self.read_file(authtoken_file)
                r = requests.get(BASE_URL + path, headers={'Authorization': 'Token ' + token})
                return r.json()
            except Exception as e:
                print 'An error occured. Send this to your administrator: ' + str(e)

        else:
            return self.auth_failed()

    def post(self, path, data):
        home_directory = os.path.expanduser('~')
        authtoken_file = os.path.join(home_directory, '.AUTHTOKEN')
        if os.path.isfile(authtoken_file):
            try:
                token = self.read_file(authtoken_file)
                r = requests.post(BASE_URL + path, headers={'Authorization': 'Token ' + token}, data=data)
                return r
            except Exception as e:
                print 'An error occured. Send this to your administrator: ' + str(e)

        else:
            return self.auth_failed()

    def auth_failed(self):
        """
        Do something if auth failed
        :return: Status and message
        """
        sys.exit("You aren't authenticated yet. Please use the login or register command to do so.")
        return (403, 'Authentication failed')

    def read_file(self, filename):
        """
        Read a file with given filename
        :param filename: String
        :return: File content
        """
        with open(filename, 'r') as (f):
            return f.read()

    def check_reponse(self, r, success, error='There was an error with your request. Please use the --help function or contact the administrator.'):
        if r.status_code == 200 and r.text != '400' and r.content != 403:
            print str(success)
        else:
            print str(error)