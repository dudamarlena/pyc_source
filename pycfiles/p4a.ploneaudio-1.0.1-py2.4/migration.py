# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/ataudio/migration.py
# Compiled at: 2007-11-27 08:53:01
import os, tempfile
from zope import interface
from zope import component
from zope import event
from zope.app.event import objectevent
from p4a.audio.migration import IMigratable
from p4a.fileimage import utils as fileutils
from Products.ExternalStorage import filewrapper

class ATAudioMigratable(object):
    __module__ = __name__
    interface.implements(IMigratable)

    def __init__(self, container, context):
        self.container = container
        self.context = context

    def migrate(self):
        orig_id = self.context.getId()
        orig_obj = self.context.aq_base
        file = orig_obj.getRawFile()
        if isinstance(file, filewrapper.FileWrapper):
            (fd, tempfilename) = tempfile.mkstemp('.mp3', 'ATAudioMigratable__temp__')
            f = open(tempfilename, 'wb')
            for x in file.filestream():
                f.write(x)

            f.close()
        else:
            tempfilename = fileutils.write_to_tempfile(file)
        self.container.manage_delObjects([orig_id])
        self.container.invokeFactory('File', orig_id)
        file = self.container[orig_id]
        f = open(tempfilename, 'rb')
        file.setFile(f)
        f.close()
        os.remove(tempfilename)
        evt = objectevent.ObjectModifiedEvent(file)
        event.notify(evt)
        return True