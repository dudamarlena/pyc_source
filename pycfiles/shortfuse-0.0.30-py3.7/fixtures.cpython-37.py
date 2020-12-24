# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/shortfuse_test/fixtures.py
# Compiled at: 2019-03-06 13:38:27
# Size of source mod 2**32: 553 bytes
import random, string, tempfile, pytest

def build_random_string(length):
    return ''.join((random.choice(string.ascii_uppercase + string.digits) for _ in range(length)))


@pytest.fixture
def random_string(length):
    return build_random_string(length)


@pytest.fixture(scope='module')
def temp_dir_module():
    return tempfile.mkdtemp(prefix='shortfuse')


@pytest.fixture
def temp_file(file_path):
    file_content = build_random_string(50)
    with open(file_path, 'w+') as (file_handle):
        file_handle.write(file_content)