# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/ConsoleEcho.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.Util.Console import ConsoleEchoer as __ConsoleEchoer
Deprecate.deprecationWarning('Use Kamaelia.Util.Console instead of Kamaelia.Util.ConsoleEcho')
consoleEchoer = Deprecate.makeClassStub(__ConsoleEchoer, 'Use Kamaelia.Util.Console:ConsoleEchoer instead of Kamaelia.Util.ConsoleEcho:consoleEchoer', 'WARN')