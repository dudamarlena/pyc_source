# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/SimpleVideoCookieServer.py
# Compiled at: 2008-10-19 12:19:52
"""
Simple Video based fortune cookie server

To watch the video, on a linux box do this:

netcat <server ip> 1500 | plaympeg -2 -

"""
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Axon.Component import component, scheduler, linkage, newComponent
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
import sys

class HelloServer(component):
    Inboxes = [
     'datain', 'inbox', 'control']
    Outboxes = ['outbox']
    maxid = 0

    def __init__(self, filename='Ulysses', debug=0):
        self.filename = filename
        self.debug = debug
        super(HelloServer, self).__init__()

    def initialiseComponent(self):
        myDataSource = ReadFileAdaptor(filename='/video/sample-100.mpg', readmode='bitrate', bitrate=375000, chunkrate=24)
        linkage(myDataSource, self, 'outbox', 'datain', self.postoffice)
        self.addChildren(myDataSource)
        return newComponent(myDataSource)

    def handleDataIn(self):
        if self.dataReady('datain'):
            data = self.recv('datain')
            if self.debug:
                sys.stdout.write(data)
            self.send(data, 'outbox')
        return 1

    def handleInbox(self):
        if self.dataReady('inbox'):
            data = self.recv('inbox')
            self.send(data, 'outbox')
        return 1

    def mainBody(self):
        self.handleDataIn()
        self.handleInbox()
        return 1


__kamaelia_components__ = (
 HelloServer,)
if __name__ == '__main__':
    SimpleServer(protocol=HelloServer, port=5222).activate()
    scheduler.run.runThreads(slowmo=0)