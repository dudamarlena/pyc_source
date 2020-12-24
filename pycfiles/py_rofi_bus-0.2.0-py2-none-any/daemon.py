# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py_rofi_bus/dbus/daemon.py
# Compiled at: 2018-06-03 14:06:06
from pydbus import SessionBus
from pydbus.bus import Bus
from gi.repository.GLib import MainLoop
from py_rofi_bus.components.mixins import ManagesProcesses

class Daemon(ManagesProcesses):
    INTERFACE_NAME = 'pro.wizardsoftheweb.pyrofibus.daemon'
    dbus = ("\n    <node>\n        <interface name='{}'>\n            <method name='is_running'>\n                <arg type='b' name='response' direction='out'/>\n            </method>\n            <method name='start'>\n            </method>\n            <method name='stop'>\n            </method>\n            <method name='load_apps'>\n                <arg type='i' name='response' direction='out'/>\n            </method>\n        </interface>\n    </node>\n    ").format(INTERFACE_NAME)
    _is_running = False

    def __init__(self, bus=None, loop=None, *args, **kwargs):
        super(Daemon, self).__init__(*args, **kwargs)
        self.initialize_bus(bus, loop)

    def initialize_bus(self, bus=None, loop=None):
        if bus is None:
            self.bus = SessionBus()
        else:
            self.bus = bus
        if loop is None:
            self.loop = MainLoop()
        else:
            self.loop = loop
        self.bus.publish(self.INTERFACE_NAME, self)
        return

    def start(self):
        if not self._is_running:
            try:
                self._is_running = True
                self.loop.run()
            except KeyboardInterrupt:
                self.loop.quit()
                self._is_running = False

    def is_running(self):
        return self._is_running

    def stop(self):
        self.loop.quit()
        self._is_running = False

    def load_apps(self):
        old_length = len(self.managed_processes)
        new_scripts = self.check_for_new_scripts()
        self.load_new_scripts(new_scripts)
        new_length = len(self.managed_processes)
        return new_length - old_length

    @classmethod
    def bootstrap(cls):
        daemon = cls()
        daemon.start()


if '__main__' == __name__:
    Daemon.bootstrap()