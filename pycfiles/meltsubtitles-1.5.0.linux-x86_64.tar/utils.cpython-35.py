# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ralph/bin/python/python35/lib/python3.5/site-packages/meltsubtitles/utils.py
# Compiled at: 2017-04-04 07:57:59
# Size of source mod 2**32: 1955 bytes
import argparse, errno, os
__author__ = 'celhipc'

def mkdir(path, mode=511):
    """
    Create subdirectory hierarchy given in the paths argument.
    Ripped from https://github.com/coursera-dl/
    """
    try:
        os.makedirs(path, mode)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def parse_args():
    """

    :return args:
    """
    parser = argparse.ArgumentParser(description='melt subtitles')
    parser.add_argument('subtitle', nargs='+', help='subtitle')
    parser.add_argument('-e', dest='ch', action='store_false', default=True, help='指定中文释义还是英文释义')
    parser.add_argument('-2', dest='sec', action='store_true', default=False, help='是否二刷')
    parser.add_argument('-w', dest='wordsrepo', action='store', nargs='+', default=[
     './wordsRepo/en5000x.csv'], help='specify the words repo')
    parser.add_argument('-p', dest='path', action='store', default='.', help='path to save the files')
    parser.add_argument('-o', '--overwrite', dest='overwrite', action='store_true', default=False, help='whether existing files should be overwritten (default: False)')
    args = parser.parse_args()
    return args