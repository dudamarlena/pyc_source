# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/exif_utils/utils.py
# Compiled at: 2018-10-28 02:47:45
# Size of source mod 2**32: 935 bytes
import subprocess, os, re

def _exec(command):
    subprocess.call(command.split())


def move_to_lower(filepaths):
    for filepath in filepaths:
        extension = filepath.split('.')[(-1)]
        if extension.islower():
            pass
        else:
            if not os.path.exists(filepath):
                pass
            else:
                next_filepath = '{}.{}'.format(filepath[:filepath.rfind('.')], extension.lower())
                command = 'mv {} {}'.format(filepath, next_filepath)
                _exec(command)


def get_image_filepaths(directory_path):
    image_extension_pattern = re.compile('([jJ][pP][eE]?[gG])|([pP][nN][gG])')
    filepaths = []
    for filename in os.listdir(directory_path):
        extension = filename.split('.')[(-1)]
        if image_extension_pattern.match(extension):
            filepaths.append(os.path.join(os.path.abspath(directory_path), filename))

    return filepaths