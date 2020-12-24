# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/conf.py
# Compiled at: 2017-02-17 21:50:27
from plasma.conf_parser import parameters
import os, errno
if os.path.exists('./conf.yaml'):
    conf = parameters('./conf.yaml')
elif os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf.yaml')):
    conf = parameters(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf.yaml'))
else:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'conf.yaml')