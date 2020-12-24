# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/projects/udt4twisted/twisted/plugins/udtplugin.py
# Compiled at: 2013-02-11 15:09:33
from twisted.application.reactors import Reactor
from twisted.application.service import ServiceMaker
udtepoll = Reactor('udtepoll', 'udt4twisted.udtepollreactor', 'UDT epoll reactor.')