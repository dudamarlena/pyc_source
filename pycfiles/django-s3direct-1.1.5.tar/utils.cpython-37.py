# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/s3direct/utils.py
# Compiled at: 2019-07-27 06:21:33
# Size of source mod 2**32: 2615 bytes
import hashlib, hmac
from collections import namedtuple
from django.conf import settings
try:
    from botocore import session
except ImportError:
    session = None

AWSCredentials = namedtuple('AWSCredentials', [
 'token', 'secret_key', 'access_key'])

def get_s3direct_destinations():
    """Returns s3direct destinations.

    NOTE: Don't use constant as it will break ability to change at runtime.
    """
    return getattr(settings, 'S3DIRECT_DESTINATIONS', None)


def sign(key, message):
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).digest()


def get_aws_v4_signing_key(key, signing_date, region, service):
    datestamp = signing_date.strftime('%Y%m%d')
    date_key = sign(('AWS4' + key).encode('utf-8'), datestamp)
    k_region = sign(date_key, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


def get_aws_v4_signature(key, message):
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()


def get_key(key, file_name, dest):
    if hasattr(key, '__call__'):
        fn_args = [file_name]
        args = dest.get('key_args')
        if args:
            fn_args.append(args)
        object_key = key(*fn_args)
    else:
        if key == '/':
            object_key = file_name
        else:
            object_key = '%s/%s' % (key.strip('/'), file_name)
    return object_key


def get_aws_credentials():
    access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    if access_key:
        if secret_key:
            return AWSCredentials(None, secret_key, access_key)
    else:
        return session or AWSCredentials(None, None, None)
    creds = session.get_session().get_credentials()
    if creds:
        return AWSCredentials(creds.token, creds.secret_key, creds.access_key)
    return AWSCredentials(None, None, None)