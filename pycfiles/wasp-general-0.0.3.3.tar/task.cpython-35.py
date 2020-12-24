# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/beacon/task.py
# Compiled at: 2017-06-28 07:14:23
# Size of source mod 2**32: 2201 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.task.thread import WThreadTask
from wasp_general.network.beacon.beacon import WNetworkServerBeacon

class WNetworkBeaconTask(WNetworkServerBeacon, WThreadTask):
    __doc__ = ' Convenient way to start WNetworkBeacon server side\n\n\tsee :class:`.WNetworkServerBeacon`\n\t'

    def __init__(self, config=None, config_section=None, thread_name=None, messenger=None):
        """ Create new threaded task

                :param config: same as config in :meth:`.WNetworkServerBeacon.__init__` method
                :param config_section: same as config_section in :meth:`.WNetworkServerBeacon.__init__` method
                :param thread_name: same as thread_name in :meth:`.WThreadTask.__init__` method
                :param messenger: same as messenger in :meth:`.WNetworkServerBeacon.__init__` method
                """
        WNetworkServerBeacon.__init__(self, config=config, config_section=config_section, messenger=messenger)
        WThreadTask.__init__(self, thread_name=thread_name)

    def start(self):
        WThreadTask.start(self)

    def stop(self):
        WThreadTask.stop(self)

    def thread_started(self):
        WNetworkServerBeacon.start(self)

    def thread_stopped(self):
        WNetworkServerBeacon.stop(self)