# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/__init__.py
# Compiled at: 2018-09-02 06:09:54
from __future__ import print_function
from .ssdp import *
from .upnp_control_point import *
from .upnp_server import *
import logging
logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] %(name)s %(levelname).1s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')