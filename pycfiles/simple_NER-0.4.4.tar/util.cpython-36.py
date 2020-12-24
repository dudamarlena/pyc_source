# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/util.py
# Compiled at: 2020-03-22 14:24:00
# Size of source mod 2**32: 1635 bytes
from os.path import join, dirname, isfile, expanduser, isdir
from os import listdir

def resolve_resource_file(res_name, lang='en-us'):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for simple_NER/res/res_name first, and
    if not found will look in language subfolders

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """
    if isfile(res_name):
        return res_name
    else:
        data_dir = join(dirname(__file__), 'res')
        filename = expanduser(join(data_dir, res_name))
        if isfile(filename):
            return filename
        data_dir = join(dirname(__file__), 'res', lang)
        filename = expanduser(join(data_dir, res_name))
        if isfile(filename):
            return filename
        data_dir = join(dirname(__file__), 'res', lang.split('-')[0])
        filename = expanduser(join(data_dir, res_name))
        if isfile(filename):
            return filename
    data_dir = join(dirname(__file__), 'res')
    for folder in listdir(data_dir):
        if folder.startswith(lang.split('-')[0]):
            filename = expanduser(join(data_dir, folder, res_name))
            if isfile(filename):
                return filename