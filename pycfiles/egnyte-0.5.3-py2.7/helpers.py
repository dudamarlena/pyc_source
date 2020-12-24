# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/tests/helpers.py
# Compiled at: 2017-03-15 09:46:43
import os

def upload_file(egnyte, filename, cloud_file_path):
    source = open(get_file_path(filename), 'rb')
    uploaded_file = egnyte.file(cloud_file_path)
    uploaded_file.upload(source)
    return uploaded_file


def get_file_path(filename):
    return os.path.join(os.getcwd(), 'egnyte', 'tests', 'data', filename)