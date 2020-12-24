# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/tests/test_monitor_plugins.py
# Compiled at: 2015-05-06 05:03:08
import unittest, time
from ConfigParser import ConfigParser
from funkload.MonitorPlugins import MonitorPlugins

class TestMonitorPlugins(unittest.TestCase):
    default_plugins = [
     'MonitorCPU', 'MonitorNetwork', 'MonitorMemFree', 'MonitorCUs']

    def test_register_default(self):
        """ Make sure all default plugins are loaded """
        p = MonitorPlugins()
        p.registerPlugins()
        plugins_loaded = p.MONITORS.keys()
        for plugin in self.default_plugins:
            self.assertTrue(plugin in plugins_loaded)

    def test_getStat(self):
        """ Make sure getStat does not raise any exception """
        p = MonitorPlugins()
        p.registerPlugins()
        for plugin in self.default_plugins:
            p.MONITORS[plugin].getStat()

    def test_network(self):
        """ Make sure self.interface is properly read from config in MonitorNetwork plugin """
        conf = ConfigParser()
        conf.add_section('server')
        conf.set('server', 'interface', 'eth9')
        p = MonitorPlugins(conf)
        p.registerPlugins()
        self.assertTrue(p.MONITORS['MonitorNetwork'].interface == 'eth9')

    def test_MonitorInfo(self):
        """ Make sure Monitor.MonitorInfo still works with plugins """
        from funkload.Monitor import MonitorInfo
        p = MonitorPlugins()
        p.registerPlugins()
        m = MonitorInfo('somehost', p)
        self.assertTrue(m.host == 'somehost')

    def test_MonitorThread(self):
        """ Make sure Monitor.MonitorThread still works with plugins """
        from funkload.Monitor import MonitorThread
        p = MonitorPlugins()
        p.registerPlugins()
        records = []
        monitor = MonitorThread(records, p, 'localhost', 1)
        monitor.start()
        monitor.startRecord()
        time.sleep(3)
        monitor.stopRecord()
        monitor.stop()
        self.assertTrue(len(records) > 0)


if __name__ == '__main__':
    unittest.main()