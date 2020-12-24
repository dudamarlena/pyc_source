# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperswitch/windows.py
# Compiled at: 2017-09-16 21:27:12


class ActiveWindowRepository(object):
    _exclusion_list = [
     None, 'Desktop']

    def __init__(self, wm_interface):
        self._wm_interface = wm_interface

    def load_windows(self):
        clients = self._wm_interface.getClientListStacking()
        windows = []
        for client in clients:
            name = self._wm_interface.getWmName(client)
            if name not in ActiveWindowRepository._exclusion_list:
                windows.append(Window(self._wm_interface, client, name))

        windows.reverse()
        return windows


class Window(object):

    def __init__(self, wm_interface, wm_id, title):
        self._wm_interface = wm_interface
        self.id = wm_id
        self.title = title

    def bring_to_front(self):
        print 'Bring to front: ' + self.title
        self._wm_interface.setActiveWindow(self.id)
        self._wm_interface.display.flush()

    def __str__(self):
        return '<Window: ' + self.title + '>'