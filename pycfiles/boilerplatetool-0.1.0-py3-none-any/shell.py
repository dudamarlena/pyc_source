# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jqb/projects/boilerplate/boilerplate/shell.py
# Compiled at: 2018-08-06 09:41:19
import os, errno, os.path as ospath

def mkdir_p(*path):
    try:
        os.makedirs(ospath.join(*path))
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def mkdir(*path):
    os.makedirs(ospath.join(*path))


def rm_maches(path, patterns=None):
    patterns = patterns or []

    def match_to_remove(name):
        for p in patterns:
            if p.match(name):
                return True

        return False

    for dirname, dirlist, filelist in os.walk(path):
        for f in filelist:
            apath = ospath.join(dirname, f)
            if match_to_remove(apath):
                os.remove(apath)