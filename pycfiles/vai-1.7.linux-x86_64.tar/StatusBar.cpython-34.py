# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/widgets/StatusBar.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2255 bytes
from .. import models
from vaitk import gui, core, utils

class StatusBar(gui.VLabel):

    def __init__(self, parent):
        super().__init__('', parent)
        self._filename = ''
        self._file_changed_flag = False
        self._position = ''
        self._message = ''
        self._remove_message_timer = core.VTimer()
        self._remove_message_timer.setSingleShot(True)
        self._remove_message_timer.timeout.connect(self.clearMessage)
        fg_color = gui.VGlobalColor.nameToColor(models.Configuration.get('colors.status_bar.fg'))
        bg_color = gui.VGlobalColor.nameToColor(models.Configuration.get('colors.status_bar.bg'))
        self.setColors(fg_color, bg_color)

    def setMessage(self, message, timeout=None):
        if self._remove_message_timer.isRunning():
            self._remove_message_timer.stop()
        if message is None:
            self.clearMessage()
            return
        self._message = message
        self._updateText()
        if timeout is not None:
            self._remove_message_timer.setInterval(timeout)
            self._remove_message_timer.start()

    def clearMessage(self):
        self._message = ''
        self._updateText()

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, pos):
        self._position = str(pos[0]) + ',' + str(pos[1])
        self._updateText()

    def setFileChangedFlag(self, changed):
        self._file_changed_flag = changed
        self._updateText()

    def _updateText(self):
        if self._filename == None:
            filename = '[No Name]'
        else:
            filename = self._filename
        if len(filename) > int(self.width() / 2):
            filename = '<' + filename[-int(self.width() / 2):]
        if self._message == '':
            self.setText(utils.strformat([(0, filename),
             (
              len(filename) + 1, '[+]' if self._file_changed_flag else '   '),
             (
              self.width() - len(self._position) - 3, self._position)], self.width()))
        else:
            self.setText(utils.strformat([(0, self._message)], self.width()))