# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/.virtualenvs/vpr/lib/python2.7/site-packages/color_helpers/__init__.py
# Compiled at: 2014-04-08 08:25:07
from path_helpers import path

def get_data_directory():
    return path(__path__[0]).joinpath('data').abspath()