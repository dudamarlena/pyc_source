# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorgui/minitorgui/lib/helpers.py
# Compiled at: 2020-03-03 11:06:13
# Size of source mod 2**32: 6789 bytes
"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging
from time import sleep
from ..minitorguiexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-12-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
LOGGER_BASENAME = 'helpers'
LOGGER = logging.getLogger(LOGGER_BASENAME)

class LoggerMixin:
    __doc__ = 'Contains a logger method for use by other classes.'

    def __init__(self):
        """____________."""
        logger_basename = 'minitorgui'
        self._logger = logging.getLogger(f"{logger_basename}.{self.__class__.__name__}")


class TunnelAdapter:
    __doc__ = '_________.'

    def __init__(self, object_, shape):
        """____________."""
        self.object_ = object_
        self.shape = shape

    def __str__(self):
        return 'Tunnel'

    def close(self):
        """____________."""
        self.shape.dim(line=True)
        return self.object_.close()


class MachineAdapter:
    __doc__ = '___________.'

    def __init__(self, object_, shape):
        """____________."""
        self.object_ = object_
        self.shape = shape

    def __str__(self):
        return 'Machine'

    def stop(self):
        """____________."""
        self.shape.dim()
        return self.object_.stop()


class BootstrapAgentAdapter:
    __doc__ = '____________.'

    def __init__(self, object_, shape):
        """____________."""
        self.object_ = object_
        self.shape = shape

    def __str__(self):
        return 'BootstrapAgent'

    def remove(self):
        """____________."""
        self.shape.dim()
        return self.object_.remove()


def setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine, machine_shape, tunnel_shape, agent_shape):
    """Starts instantiated TransferAgents, opens instantiated Tunnel(s) and starts instantiated Machine(s).

    This function also passes the instantiated objects to the StateManager, which
    will stop Machines and close Tunnels after a KeyboardInterrupt (by the user
    or by the program in COMMAND and FILE mode).

    Args:
        state (StateManager): An instantiated StateManager object.
        transfer_agent (TransferAgent): An instantiated TransferAgent object.
        bootstrap_agent (BootstrapAgent): <>
        tunnel (Tunnel): An instantiated Tunnel object.
        machine (Machine): An instantiated Machine object.
        machine_shape (): <>
        tunnel_shape (): <>
        agent_shape (): <>

    """
    agent_shape.show()
    agent_shape.move()
    if not transfer_agent.start():
        agent_shape.transfer_nok()
        raise SetupFailed(transfer_agent)
    if transfer_agent.__class__.__name__ == 'FirstTransferAgent':
        LOGGER.info('Agent transferred to %s ', machine.hostname)
    else:
        if transfer_agent.__class__.__name__ == 'ConsecutiveTransferAgent':
            LOGGER.info('Agent transferred through Tunnel to %s ', machine.hostname)
        else:
            agent_shape.transfer_ok()
            tunnel_shape.show()
            state.add_object(TunnelAdapter(tunnel, tunnel_shape))
            if not tunnel.open():
                tunnel_shape.setup_nok()
                raise SetupFailed(tunnel)
            LOGGER.info('Tunnel opened (%s)', tunnel.ip_address_i)
            tunnel_shape.setup_ok(line=True)
            state.add_object(BootstrapAgentAdapter(bootstrap_agent, agent_shape))
            if not bootstrap_agent.start():
                agent_shape.setup_nok()
                raise SetupFailed(bootstrap_agent)
            LOGGER.info('Agent is executed')
            agent_shape.setup_ok()
            sleep(0.2)
            state.add_object(MachineAdapter(machine, machine_shape))
            machine.start() or machine_shape.setup_nok()
            raise SetupFailed(machine)
        LOGGER.info('Machine started (%s)', machine.hostname)
        machine_shape.setup_ok()
        sleep(0.2)


class ConnectionVisualizer:
    __doc__ = 'Shows the state of the encrypted tunnel.'

    def __init__(self, animate_connection, heartbeat):
        """____________."""
        self.animate_connection = animate_connection
        self.heartbeat = heartbeat

    def start(self):
        """_____________."""
        self.animate_connection.start()
        while not self.heartbeat.terminate:
            if not self.heartbeat.is_tunnel_intact:
                self.animate_connection.broken()
                while not self.heartbeat.is_tunnel_intact:
                    sleep(0.2)

                self.animate_connection.restored()
            sleep(0.2)

        self.animate_connection.stop()