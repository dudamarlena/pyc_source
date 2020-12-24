# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/idavoll.py
# Compiled at: 2009-06-18 09:05:11
try:
    from twisted.application.service import ServiceMaker
except ImportError:
    from twisted.scripts.mktap import _tapHelper as ServiceMaker

Idavoll = ServiceMaker('Idavoll', 'idavoll.tap', 'Jabber Publish-Subscribe Service Component', 'idavoll')