# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/orpheus/Desarrollo/yaml2html/yatom/tests/resources/__init__.py
# Compiled at: 2019-03-27 18:36:02
try:
    import importlib.resources as res
except ImportError:
    import importlib_resources as res

def contents():
    return res.contents(__name__)


def read_text(resource, encoding='utf-8'):
    return res.read_text(__name__, resource, encoding=encoding)