# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nikhila/mp_projs/pj/pj/peeldb/management/commands/push_webpack_files.py
# Compiled at: 2017-04-08 04:18:55
# Size of source mod 2**32: 8310 bytes
from django.core.management.base import BaseCommand
from django.core.management import call_command
import json, subprocess
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import mimetypes, os
from os import path
import hashlib
from datetime import datetime
import boto
from django.core.management.base import BaseCommand
from django.core.management import call_command
import json, subprocess
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import mimetypes, os
from os import path
import hashlib
from datetime import datetime
import boto

def call_subprocess(command):
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(proc.communicate())


def upload_to_s3(css_file):
    bucket_name = 'peeljobs'
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    folder = 'webpack_bundles/'
    bucket = conn.get_bucket(bucket_name=bucket_name)
    filename = css_file.split('/')[(-1)]
    file_obj = open(css_file, 'r')
    content = file_obj.read()
    key = folder + filename
    print('aws file name')
    print(filename)
    bucket = conn.get_bucket(bucket_name=bucket_name)
    mime = mimetypes.guess_type(filename)[0]
    k = Key(bucket)
    print(key)
    k.key = key
    k.set_metadata('Content-Type', mime)
    k.set_contents_from_string(content)
    public_read = True
    if public_read:
        k.set_acl('public-read')


class Command(BaseCommand):
    args = '<filename>'
    help = 'Loads the initial data in to database'

    def handle(self, *args, **options):
        call_subprocess('./node_modules/.bin/webpack --config webpack.config.js')
        for each in settings.WEB_PACK_FILES:
            print(each['html_file_name'])
            print(each['webpack_js'] + '-*' + '.css')
            directory = settings.BASE_DIR + '/static/webpack_bundles/'
            css_file = max([os.path.join(directory, d) for d in os.listdir(directory) if d.startswith(each['webpack_js']) and d.endswith('css')], key=os.path.getmtime)
            js_file = max([os.path.join(directory, d) for d in os.listdir(directory) if d.startswith(each['webpack_js']) and d.endswith('js')], key=os.path.getmtime)
            print(css_file)
            print(js_file)
            upload_to_s3(css_file)
            upload_to_s3(js_file)
            import re
            regex = '(.*?<link rel="stylesheet" type="text/css" href=")(.*?)(" id="packer_css"/>.*?<script id="packer_js" src=")(.*?)(" type="text/javascript"></script>.*)'
            with open('templates/base.html', 'r+') as (f):
                content = f.read()
                m = re.match(regex, content, re.DOTALL)
                href = settings.STATIC_URL + css_file.split('/static/')[(-1)]
                src = settings.STATIC_URL + js_file.split('/static/')[(-1)]
                content = m.group(1) + href + m.group(3) + src + m.group(5)
            with open('templates/base.html', 'w') as (f):
                f.write(content)

        result = {'message': 'Successfully Loading initial data'}
        return json.dumps(result)