# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/helpers/auth_helpers.py
# Compiled at: 2016-10-19 09:13:42
import os

def create_token_file(token):
    try:
        home_directory = os.path.expanduser('~')
        file = open(os.path.join(home_directory, '.AUTHTOKEN'), 'w')
        file.write(token['token'])
        file.close()
        return 200
    except:
        print 'Something went wrong!'


def remove_token_file():
    try:
        home_directory = os.path.expanduser('~')
        os.remove(os.path.join(home_directory, '.AUTHTOKEN'))
    except:
        print 'Something went wrong!'