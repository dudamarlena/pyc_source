# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/runner/signal_stop.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 1703 bytes
from __future__ import unicode_literals
import logging, signal
from requests.exceptions import Timeout
from ..action import ContainerUtilAction
from ..input import ItemType
log = logging.getLogger(__name__)

class SignalMixin(object):
    action_method_names = [
     (
      ItemType.CONTAINER, ContainerUtilAction.SIGNAL_STOP, 'signal_stop')]

    def signal_stop(self, action, c_name, **kwargs):
        """
        Stops a container, either using the default client stop method, or sending a custom signal and waiting
        for the container to stop.

        :param action: Action configuration.
        :type action: dockermap.map.runner.ActionConfig
        :param c_name: Container name.
        :type c_name: unicode | str
        :param kwargs: Additional keyword arguments to complement or override the configuration-based values.
        :type kwargs: dict
        """
        client = action.client
        sig = action.config.stop_signal
        stop_kwargs = self.get_container_stop_kwargs(action, c_name, kwargs=kwargs)
        if sig:
            if sig == 'SIGTERM' or sig == signal.SIGTERM:
                try:
                    (client.stop)(**stop_kwargs)
                except Timeout:
                    log.warning('Container %s did not stop in time - sent SIGKILL.', c_name)
                    try:
                        client.wait(c_name, timeout=(stop_kwargs.get('timeout', 10)))
                    except Timeout:
                        pass

        else:
            log.debug('Sending signal %s to the container %s and waiting for stop.', sig, c_name)
            client.kill(c_name, signal=sig)
            client.wait(c_name, timeout=(stop_kwargs.get('timeout', 10)))