# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/test/mocks.py
# Compiled at: 2016-10-05 04:16:49
# Size of source mod 2**32: 622 bytes
import pytest, shutil, os
from django.conf import settings
from buckets.utils import ensure_dirs

@pytest.fixture(scope='function')
def make_dirs(request):
    ensure_dirs('uploads', 'downloads', 'uploads/files')

    def teardown():
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 's3'))

    request.addfinalizer(teardown)


def create_file(subdir=None, name='text.txt'):
    path = 's3'
    if subdir:
        path += '/' + subdir
    path = os.path.join(settings.MEDIA_ROOT, path, name)
    file = open(path, 'wb')
    file.write('Some content'.encode('utf-8'))
    file.close()
    return file