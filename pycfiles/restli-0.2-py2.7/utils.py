# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/restli/utils.py
# Compiled at: 2016-02-23 17:20:39
import logging, os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('restli')

def user_input(text):
    try:
        return raw_input(text)
    except NameError:
        return input(text)


class OutputMessages(object):
    GENERATING = '\n    generating {}\n    '
    OVERWRITING = '\n    overwriting {}\n    '
    LEAVING_FILE_UNTOUCHED = '\n    leaving file untouched {}\n    '
    WOULD_YOU_LIKE_TO_OVERWRITE = '\n    It looks like there is already a file named {} within the directory {}. Would you like to overwrite it? (y/n) :\n    '
    NO_DIRECTORY_FOUND = '\n    No directory "{}" found in cwd. Please run restli --scaffold [project-name] --namespace [namespace] to generate a restli directory structure\n    '

    @staticmethod
    def tree(start_path):
        acc = ''
        for root, dirs, files in os.walk(start_path):
            level = root.replace(start_path, '').count(os.sep)
            indent = '    ' * level
            acc += ('{}{}/\n').format(indent, os.path.basename(root))
            subindent = '    ' * (level + 1)
            for f in files:
                acc += ('{}{}\n').format(subindent, f)

        return acc


def find_directory(target_name):
    for dir_name, _, _ in os.walk(os.getcwd()):
        if dir_name.endswith(target_name):
            return dir_name

    raise Exception(OutputMessages.NO_DIRECTORY_FOUND.format(dir_name))