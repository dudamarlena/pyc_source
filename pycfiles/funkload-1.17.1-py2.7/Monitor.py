# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/Monitor.py
# Compiled at: 2015-05-06 05:03:08
"""A Linux monitor server/controller.
"""
import sys
from time import time, sleep
from threading import Thread
from XmlRpcBase import XmlRpcBaseServer, XmlRpcBaseController
from MonitorPlugins import MonitorPlugins

class MonitorInfo:
    """A simple class to collect info."""

    def __init__(self, host, plugins):
        self.time = time()
        self.host = host
        for plugin in plugins.MONITORS.values():
            for key, value in plugin.getStat().items():
                setattr(self, key, value)

    def __repr__(self, extra_key=None):
        text = '<monitor '
        if extra_key is not None:
            text += 'key="%s" ' % extra_key
        for key, value in self.__dict__.items():
            text += '%s="%s" ' % (key, value)

        text += ' />'
        return text


class MonitorThread(Thread):
    """The monitor thread that collect information."""

    def __init__(self, records, plugins, host=None, interval=None):
        Thread.__init__(self)
        self.records = records
        self._recorder_count = 0
        self._running = False
        self._interval = None
        self._host = None
        self._plugins = plugins
        self.setInterval(interval)
        self.setHost(host)
        self.setDaemon(1)
        return

    def setInterval(self, interval):
        """Set the interval between monitoring."""
        self._interval = interval

    def setHost(self, host):
        """Set the monitored host."""
        self._host = host

    def run(self):
        """Thread jobs."""
        self._running = True
        while self._running:
            t1 = time()
            if self._recorder_count > 0:
                self.monitor()
            t2 = time()
            to_sleep = self._interval - (t2 - t1)
            if to_sleep > 0:
                sleep(to_sleep)

    def stop(self):
        """Stop the thread."""
        self._running = False

    def monitor(self):
        """The monitor task."""
        self.records.append(MonitorInfo(self._host, self._plugins))

    def startRecord(self):
        """Enable recording."""
        self._recorder_count += 1

    def stopRecord(self):
        """Stop recording."""
        self._recorder_count -= 1

    def countRecorders(self):
        """Return the number of recorder."""
        return self._recorder_count


class MonitorServer(XmlRpcBaseServer):
    """The XML RPC monitor server."""
    server_name = 'monitor'
    method_names = XmlRpcBaseServer.method_names + [
     'startRecord', 'stopRecord', 'getResult', 'getXmlResult', 'getMonitorsConfig']

    def __init__(self, argv=None):
        self.interval = None
        self.records = []
        self._keys = {}
        XmlRpcBaseServer.__init__(self, argv)
        self.plugins = MonitorPlugins(self._conf)
        self.plugins.registerPlugins()
        self._monitor = MonitorThread(self.records, self.plugins, self.host, self.interval)
        self._monitor.start()
        return

    def _init_cb(self, conf, options):
        """init callback."""
        self.interval = conf.getfloat('server', 'interval')
        self._conf = conf

    def startRecord(self, key):
        """Start to monitor if it is the first key."""
        self.logd('startRecord %s' % key)
        if not self._keys.has_key(key) or self._keys[key][1] is not None:
            self._monitor.startRecord()
        self._keys[key] = [
         len(self.records), None]
        return 1

    def stopRecord(self, key):
        """Stop to monitor if it is the last key."""
        self.logd('stopRecord %s' % key)
        if not self._keys.has_key(key) or self._keys[key][1] is not None:
            return 0
        self._keys[key] = [
         self._keys[key][0], len(self.records)]
        self._monitor.stopRecord()
        return 1

    def getResult(self, key):
        """Return stats for key."""
        self.logd('getResult %s' % key)
        if key not in self._keys.keys():
            return []
        ret = self.records[self._keys[key][0]:self._keys[key][1]]
        return ret

    def getMonitorsConfig(self):
        ret = {}
        for plugin in self.plugins.MONITORS.values():
            conf = plugin.getConfig()
            if conf:
                ret[plugin.name] = conf

        return ret

    def getXmlResult(self, key):
        """Return result as xml."""
        self.logd('getXmlResult %s' % key)
        ret = self.getResult(key)
        ret = [ stat.__repr__(key) for stat in ret ]
        return ('\n').join(ret)

    def test(self):
        """auto test."""
        key = 'internal_test_monitor'
        self.startRecord(key)
        sleep(3)
        self.stopRecord(key)
        self.log(self.records)
        self.log(self.getXmlResult(key))
        return 1


class MonitorController(XmlRpcBaseController):
    """Monitor controller."""
    server_class = MonitorServer

    def test(self):
        """Testing monitor server."""
        server = self.server
        key = 'internal_test_monitor'
        server.startRecord(key)
        sleep(2)
        server.stopRecord(key)
        self.log(server.getXmlResult(key))
        return 0


def main():
    """Control monitord server."""
    ctl = MonitorController()
    sys.exit(ctl())


def test():
    """Test wihtout rpc server."""
    mon = MonitorServer()
    mon.test()


if __name__ == '__main__':
    main()