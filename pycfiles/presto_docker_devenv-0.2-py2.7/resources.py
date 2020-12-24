# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/common/resources.py
# Compiled at: 2016-03-01 07:13:25
from os import path
_ROOT = path.join(path.abspath(path.dirname(__file__)), '..', '..')

def resources_path():
    return __path_safe(_ROOT, 'images')


def image_path(image):
    return __path_safe(_ROOT, 'images', image)


def __path_safe(*parts):
    resource = path.join(*parts)
    if not path.exists(resource):
        raise Exception('Resource path does not exists: %s' % resource)
    return resource