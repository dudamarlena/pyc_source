# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/adapters/framework/util.py
# Compiled at: 2015-07-24 00:09:42
# Size of source mod 2**32: 887 bytes
import functools, os, tempfile
from urllib.request import urlretrieve
from zipfile import ZipFile

def download_and_extract(zip_url):
    """
    :param zip_url: An http or https URL pointing to a zip file
    :return: the path to a temp directory containing the archive
             contents. The caller is responsible for deleting
             the temp dir.
    """
    output_dir = tempfile.mkdtemp()
    zip_path = urlretrieve(zip_url)[0]
    ZipFile(zip_path).extractall(output_dir)
    os.unlink(zip_path)
    return output_dir


def memoize(obj):
    """See https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize"""
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer