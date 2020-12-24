# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/config.py
# Compiled at: 2010-12-27 10:45:29
from os.path import dirname, abspath, join
import yaml
loader = yaml.load
from sleepy.shorties import s
from sleepy.exceptions import NotFoundException

def tipes_load_dir():
    return join(dirname(abspath(__file__)), 'yaml', 'tipes')


def loaded_tipe_node(tipe):
    try:
        return loader(open(join(tipes_load_dir(), s('{{ tipename }}.yaml', tipename=tipe.__class__.__name__.lower()))).read())
    except IOError:
        raise NotFoundException()


def static_dir():
    return join(dirname(abspath(__file__)), 'static')


def templates_dir():
    return join(dirname(abspath(__file__)), 'templates')