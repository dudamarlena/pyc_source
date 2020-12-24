# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/routesies.py
# Compiled at: 2010-11-27 18:52:15
from sleepy.shorties import s
from sleepy.controllers import default_controller

def reorder(mapper, res):
    mapper.link(rel='reorder', name=s('reorder_{{ name }}', name=mapper.resource_name), action='reorder', method='POST', controller=default_controller, names_path=res.path.names_path)


def resurrect(mapper, res):
    mapper.link(rel='resurrect', name=s('resurrect_{{ name }}', name=mapper.resource_name), action='resurrect', method='POST', controller=default_controller, names_path=res.path.names_path)


def resurrection(mapper, res):
    mapper.link(rel='resurrection', name=s('resurrection_{{ name }}', name=mapper.resource_name), action='resurrection', method='GET', controller=default_controller, names_path=res.path.names_path)