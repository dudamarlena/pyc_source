# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/FSZScheduleEvent.py
# Compiled at: 2016-01-29 02:22:17
import AccessControl
from ZScheduleEvent import ZScheduleEvent
from Products.CMFCore.FSObject import FSObject
from Products.CMFCore.DirectoryView import registerFileExtension, registerMetaType
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

class FSZScheduleEvent(FSObject, ZScheduleEvent):
    """
    A File system ZScheduleEvent
    """
    meta_type = 'FSZScheduleEvent'
    manage_options = ({'label': 'Customize', 'action': 'manage_main'},) + ZScheduleEvent.manage_options[1:-2]
    __ac_permissions__ = ZScheduleEvent.__ac_permissions__ + FSObject.__ac_permissions__
    manage_main = PageTemplateFile('zpt/fsevent', globals())

    def _createZODBClone(self):
        obj = ZScheduleEvent(self.getId(), self.title, self.callable, self.minute, self.hour, self.month, self.day_of_month, self.day_of_week, self.tz)
        return obj

    def __call__(self, *args, **kw):
        """Calls the script."""
        self._updateFromFS()
        return ZScheduleEvent.__call__(self, *args, **kw)

    def _readFile(self, reparse):
        """Read the data from the filesystem.

        Read the file (indicated by exandpath(self._filepath), and parse the
        data if necessary.
        """
        file = open(self._filepath, 'r')
        try:
            lines = file.readlines()
        finally:
            file.close()

        tz = 'UTC'
        lino = 0
        for line in lines:
            lino = lino + 1
            line = line.strip()
            if not line or line[0] == '#':
                continue
            try:
                if line.startswith('title='):
                    self.title = line[6:]
                elif line.startswith('tz='):
                    tz = line[3:]
                else:
                    self.status = 0
                    minute, hour, month, day_of_month, day_of_week, callable_id = line.split(' ')
                    self.manage_editSchedule(tz, minute, hour, month, day_of_month, day_of_week, 0)
                    self.callable_id = callable_id
            except:
                raise ValueError, 'Error processing line %s of %s:\n%s' % (lino, fp, line)


AccessControl.class_init.InitializeClass(FSZScheduleEvent)
registerFileExtension('sched', FSZScheduleEvent)
registerMetaType('ZScheduleEvent Object', FSZScheduleEvent)