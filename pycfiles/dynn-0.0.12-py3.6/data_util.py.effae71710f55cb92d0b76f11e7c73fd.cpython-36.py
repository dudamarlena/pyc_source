# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\data\data_util.py.effae71710f55cb92d0b76f11e7c73fd.py
# Compiled at: 2018-09-19 13:42:08
# Size of source mod 2**32: 1084 bytes
"""
Data utilities
==============

Helper functions to download and manage datasets.
"""
import os
from urllib.request import urlretrieve
from urllib.parse import urljoin

def download_if_not_there(file, url, path, force=False):
    """Downloads a file from the given url if and only if the file doesn't
    already exist in the provided path or ``force=True``

    Args:
        file (str): File name
        url (str): Url where the file can be found (without the filename)
        path (str): Path to the local folder where the file should be stored
        force (bool, optional): Force the file download (useful if you suspect
            that the file might have changed)
    """
    abs_path = os.path.abspath(path)
    local_file_path = os.path.join(abs_path, file)
    if force or not os.path.isfile(local_file_path):
        print(f"Downloading file {file} to folder {abs_path} from {url}")
        file_url = urljoin(url, file)
        return urlretrieve(file_url, local_file_path)