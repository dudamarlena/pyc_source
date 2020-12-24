# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/KamaeliaIPC.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.IPC import producerFinished as __producerFinished
from Kamaelia.IPC import notify as __notify
from Kamaelia.IPC import socketShutdown as __socketShutdown
from Kamaelia.IPC import newCSA as __newCSA
from Kamaelia.IPC import shutdownCSA as __shutdownCSA
from Kamaelia.IPC import newServer as __newServer
from Kamaelia.IPC import newWriter as __newWriter
from Kamaelia.IPC import newReader as __newReader
from Kamaelia.IPC import newExceptional as __newExceptional
from Kamaelia.IPC import removeReader as __removeReader
from Kamaelia.IPC import removeWriter as __removeWriter
from Kamaelia.IPC import removeExceptional as __removeExceptional
Deprecate.deprecationWarning('Use Kamaelia.IPC instead of Kamaelia.KamaeliaIPC')
producerFinished = Deprecate.makeClassStub(__producerFinished, 'Use Kamaelia.IPC:producerFinished instead of KamaeliaIPC:producerFinished', 'WARN')
notify = Deprecate.makeClassStub(__notify, 'Use Kamaelia.IPC:notify instead of Kamaelia.KamaeliaIPC:notify', 'WARN')
socketShutdown = Deprecate.makeClassStub(__socketShutdown, 'Use Kamaelia.IPC:socketShutdown instead of Kamaelia.KamaeliaIPC:socketShutdown', 'WARN')
newCSA = Deprecate.makeClassStub(__newCSA, 'Use Kamaelia.IPC: instead of Kamaelia.KamaeliaIPC:newCSA', 'WARN')
shutdownCSA = Deprecate.makeClassStub(__shutdownCSA, 'Use Kamaelia.IPC:shutdownCSA instead of Kamaelia.KamaeliaIPC:shutdownCSA', 'WARN')
newServer = Deprecate.makeClassStub(__newServer, 'Use Kamaelia.IPC:newServer instead of Kamaelia.KamaeliaIPC:newServer', 'WARN')
newWriter = Deprecate.makeClassStub(__newWriter, 'Use Kamaelia.IPC:newWriter instead of Kamaelia.KamaeliaIPC:newWriter', 'WARN')
newReader = Deprecate.makeClassStub(__newReader, 'Use Kamaelia.IPC:newReader instead of Kamaelia.KamaeliaIPC:newReader', 'WARN')
newExceptional = Deprecate.makeClassStub(__newExceptional, 'Use Kamaelia.IPC:newExceptional instead of Kamaelia.KamaeliaIPC:newExceptional', 'WARN')
removeReader = Deprecate.makeClassStub(__removeReader, 'Use Kamaelia.IPC:removeReader instead of Kamaelia.KamaeliaIPC:removeReader', 'WARN')
removeWriter = Deprecate.makeClassStub(__removeWriter, 'Use Kamaelia.IPC:removeWriter instead of Kamaelia.KamaeliaIPC:removeWriter', 'WARN')
removeExceptional = Deprecate.makeClassStub(__removeExceptional, 'Use Kamaelia.IPC:removeExceptional instead of Kamaelia.KamaeliaIPC:removeExceptional', 'WARN')
removeExceptional = Deprecate.makeClassStub(__removeExceptional, 'Use Kamaelia.IPC:removeExceptional instead of Kamaelia.KamaeliaIPC:removeExceptional', 'WARN')