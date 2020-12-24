# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/SingleServer.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.Internet.SingleServer import SingleServer as __SingleServer
Deprecate.deprecationWarning('Use Kamaelia.Internet.SingleServer instead of Kamaelia.SingleServer')
SingleServer = Deprecate.makeClassStub(__SingleServer, 'Use Kamaelia.Internet.SingleServer:SingleServer instead of Kamaelia.SingleServer:SingleServer', 'WARN')