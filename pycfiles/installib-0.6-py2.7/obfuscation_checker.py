# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/installib/obfuscation_checker.py
# Compiled at: 2016-12-13 08:17:02
import os, hashlib

def _hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()

    return sha1.hexdigest()


def _equal_hash(file1, file2):
    return _hashfile(file1) == _hashfile(file2)


def assert_not_equal_hash(path_to_file1, path_to_file2):
    assert os.path.isfile(path_to_file1), '%s not found' % path_to_file1
    assert os.path.isfile(path_to_file2), '%s not found' % path_to_file2
    assert not _equal_hash(path_to_file1, path_to_file2), 'Ups, %s and %s files are equal' % (path_to_file1,
     path_to_file2)