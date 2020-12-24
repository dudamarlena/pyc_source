# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dirutil\checksum.py
# Compiled at: 2018-12-25 04:31:32
# Size of source mod 2**32: 3531 bytes
"""Checksums for files and directories
"""
__author__ = 'Dmitri Dolzhenko'
__email__ = 'd.dolzhenko@gmail.com'
import os, hashlib
md5 = hashlib.md5
sha1 = hashlib.sha1
sha256 = hashlib.sha256
sha512 = hashlib.sha512

def is_hiddden(path):
    return bool(re.search('/\\.', path))


def walk_if(path, predicate=lambda x: True):
    for x in os.walk(path, topdown=True):
        if predicate(x):
            yield x


def hash_fs(path, hash_algo=sha1):
    if os.path.isdir(path):
        return hash_dir(path, hash_algo)
    if os.path.isfile(path):
        return hash_file(path, hash_algo)
    raise Exception('{} is not dir and not file'.format(path))


def hash_path(path, hash_algo=sha1):
    hasher = hash_algo()
    hasher.update(path.encode('utf-16').replace('\\', '/'))
    return hasher.hexdigest


def hash_dir(path, hash_algo=sha1):
    hasher = hash_algo()
    for root, dirs, files in os.walk(path, topdown=True):
        in_empty_folder = not dirs and not files
        if in_empty_folder:
            hasher.update(hash_path(root, hash_algo))
        else:
            filenames = (os.path.join(root, f) for f in files)
            hashes = (hash_file(name, hash_algo, consider_filename=True) for name in filenames)
            map(hasher.update, hashes)

    return hasher.hexdigest()


def file_blocks(f, blocksize=1024):
    while True:
        data = f.read(blocksize)
        if not data:
            break
        yield data


def hash_file(filename, hash_algo=sha1, consider_filename=False):
    hasher = hash_algo()
    if consider_filename:
        hasher.update(filename.encode('utf-16'))
    with open(filename, 'rb') as (f):
        for data in file_blocks(f, blocksize=65536):
            hasher.update(data)

    return hasher.hexdigest()


import unittest

class TestCase(unittest.TestCase):

    def test_1(self):
        folder = 'C:\\Users\\Dmitry\\Documents\\repos\\TestGit\\test'
        for x in walk_if(folder):
            print(x)