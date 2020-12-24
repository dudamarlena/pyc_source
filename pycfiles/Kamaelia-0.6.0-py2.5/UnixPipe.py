# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/UnixPipe.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.File.UnixProcess import UnixProcess as __UnixProcess
Deprecate.deprecationWarning('Use Kamaelia.File.UnixProcess instead of Kamaelia.File.UnixPipe')
Pipethrough = Deprecate.makeClassStub(__UnixProcess, 'Use Kamaelia.File.UnixProcess:UnixProcess instead of Kamaelia.File.UnixPipe:Pipethrough', 'WARN')