# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/WholeFileWriter.py
# Compiled at: 2008-10-19 12:19:52
"""=======================
Whole File Writer
=======================

This component accepts file creation jobs and signals the completion of each
jobs. Creation jobs consist of a list [ filename, contents ] added to "inbox".
Completion signals consist of the string "done" being sent to "outbox".

All jobs are processed sequentially.

This component does not terminate.
"""
from Axon.Component import component

class WholeFileWriter(component):
    """    WholeFileWriter() -> component that creates and writes files 
    
    Uses [ filename, contents ] structure to file creation messages in "inbox"
    """
    Inboxes = {'inbox': 'file creation jobs', 
       'control': 'UNUSED'}
    Outboxes = {'outbox': 'filename written', 
       'signal': 'UNUSED'}

    def __init__(self):
        super(WholeFileWriter, self).__init__()

    def writeFile(self, filename, data):
        """Writes the data to a new file"""
        file = open(filename, 'wb', 0)
        data = file.write(data)
        file.close()

    def main(self):
        """Main loop"""
        while 1:
            yield 1
            if self.dataReady('inbox'):
                command = self.recv('inbox')
                self.writeFile(command[0], command[1])
                self.send(command[0], 'outbox')
            else:
                self.pause()


__kamaelia_components__ = (
 WholeFileWriter,)