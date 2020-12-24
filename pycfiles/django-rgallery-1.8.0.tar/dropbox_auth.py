# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/Peques/src/peques/management/commands/dropbox_auth.py
# Compiled at: 2013-04-18 11:24:55
import os, errno
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
from dropbox import client, rest, session

class Command(BaseCommand):
    help = '\n    Tool that tries to parse the photos, saving it on the database and\n    converting the photos to fit the web:\n\n    ./manage.py parse_photos\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        APP_KEY = 'ba0nqlc4231mtjq'
        APP_SECRET = '81uj883ozr4ytff'
        ACCESS_TYPE = 'app_folder'
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        print 'url:', url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()
        access_token = sess.obtain_access_token(request_token)
        print access_token.key
        print access_token.secret
        client = client.DropboxClient(sess)
        print 'linked account:', client.account_info()