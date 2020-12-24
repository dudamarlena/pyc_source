# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/timers/Crontab/Crontab.py
# Compiled at: 2015-07-18 19:40:58
import subprocess, logging, AccessControl
from AccessControl.Permissions import view, change_configuration
from Products.ZScheduler.interfaces.ITimer import ITimer
from Products.ZScheduler.timers.Base import ThreadedTimer
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
log = logging.getLogger('ZScheduler.Crontab')

class Crontab(ThreadedTimer):
    """
    A crontab dispatching mechanism
    """
    meta_type = 'Crontab'
    __implements__ = (ITimer,)
    __ac_permissions__ = ThreadedTimer.__ac_permissions__ + (
     (
      change_configuration, ('manage_load', 'manage_unload')),
     (
      view, ('index_html', )))
    property_extensible_schema__ = 0
    _properties = ThreadedTimer._properties + ({'id': 'command', 'mode': 'w', 'type': 'string'},)
    manage_options = (
     {'label': 'Properties', 'action': 'manage_propertiesForm', 'help': ('ZScheduler', 'crontab.stx')}, {'label': 'View', 'action': ''}) + ThreadedTimer.manage_options[1:]
    manage_main = ThreadedTimer.manage_propertiesForm

    def __init__(self):
        ThreadedTimer.__init__(self)
        self.command = 'wget -q --tries=1 --user=admin --password=secret --auth-no-challenge -O /dev/null'

    index_html = PageTemplateFile('zpt/crontab', globals())

    def _load(self):
        """
        physically install our crontab
        """
        crontab = self.index_html()
        log.info(crontab)
        try:
            pipe = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError as e:
            log.error(str(e))
            return

        output = pipe.communicate(crontab)
        if output:
            log.error('load error: %s' % str(output))

    def manage_load(self, REQUEST=None):
        """
        """
        self._load()
        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Load crontab')
            return self.manage_main(self, REQUEST)

    def _unload(self):
        """
        remove our system crontab
        """
        try:
            pipe = subprocess.Popen(['crontab', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            log.error(e)
            return

        output, errors = pipe.communicate()
        if output:
            log.error(output)

    def manage_unload(self, REQUEST=None):
        """
        """
        self._unload()
        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Unloaded crontab')
            return self.manage_main(self, REQUEST)

    def manage_editProperties(self, command, is_active=False, REQUEST=None):
        """
        change all properties, then tell ZScheduler to reload crontab ...
        """
        old_is_active = self.is_active
        old_command = self.command
        self._updateProperty('is_active', is_active)
        self._updateProperty('command', command)
        if old_command != command:
            if old_is_active and is_active:
                self.manage_restart()
        if is_active:
            if not old_is_active:
                self._start()
            else:
                self._stop()
        self.aq_parent.semaphore.set()
        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Properties Updated')
            return self.manage_propertiesForm(self, REQUEST)

    def isActive(self):
        """
        verify the crontab is installed
        """
        try:
            pipe = subprocess.Popen(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            return False

        output, errors = pipe.communicate()
        if output and len(output) > 25:
            return True
        return False


AccessControl.class_init.InitializeClass(Crontab)