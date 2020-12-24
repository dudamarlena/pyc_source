# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/utils.py
# Compiled at: 2016-07-22 10:43:27
# Size of source mod 2**32: 1253 bytes
import os, string, random
from django.conf import settings

def validate_settings():
    assert settings.AWS, 'No AWS settings found'
    assert settings.AWS.get('ACCESS_KEY'), 'AWS access key is not set in settings'
    assert settings.AWS.get('SECRET_KEY'), 'AWS secret key is not set in settings'
    assert settings.AWS.get('BUCKET'), 'AWS bucket name is not set in settings'


ID_FIELD_LENGTH = 24
alphabet = string.ascii_lowercase + string.digits
alphabet0 = string.ascii_lowercase + string.ascii_lowercase
for loser in 'l1o0':
    i = alphabet.index(loser)
    alphabet = alphabet[:i] + alphabet[i + 1:]

for loser in 'lo':
    i = alphabet0.index(loser)
    alphabet0 = alphabet0[:i] + alphabet0[i + 1:]

def byte_to_base32_chr(byte):
    return alphabet[(byte & 31)]


def byte_to_letter(byte):
    return alphabet0[(byte & 31)]


def random_id():
    rand_id = [random.randint(0, 255) for i in range(ID_FIELD_LENGTH)]
    return byte_to_letter(rand_id[0]) + ''.join(map(byte_to_base32_chr, rand_id[1:]))


def ensure_dirs(*args):
    for dir in args:
        path = os.path.join(settings.MEDIA_ROOT, 's3', dir)
        if not os.path.exists(path):
            os.makedirs(path)