# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protocol.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 7765 bytes
__doc__ = 'Implementation of the MRP protocol.'
import asyncio, uuid, logging
from collections import namedtuple
from pyatv.mrp import messages, protobuf
from pyatv.mrp.pairing import MrpPairingVerifier
from pyatv.mrp.srp import Credentials
_LOGGER = logging.getLogger(__name__)
Listener = namedtuple('Listener', 'func data')
OutstandingMessage = namedtuple('OutstandingMessage', 'semaphore response')

class MrpProtocol:
    """MrpProtocol"""

    def __init__(self, loop, connection, srp, service):
        """Initialize a new MrpProtocol."""
        self.loop = loop
        self.connection = connection
        self.connection.listener = self
        self.srp = srp
        self.service = service
        self._outstanding = {}
        self._listeners = {}
        self._one_shots = {}
        self._initial_message_sent = False

    def add_listener(self, listener, message_type, data=None, one_shot=False):
        """Add a listener that will receice incoming messages."""
        lst = self._one_shots if one_shot else self._listeners
        if message_type not in lst:
            lst[message_type] = []
        lst[message_type].append(Listener(listener, data))

    async def start(self):
        """Connect to device and listen to incoming messages."""
        if self.connection.connected:
            return
        else:
            await self.connection.connect()
            if self.service.device_credentials:
                self.srp.pairing_id = Credentials.parse(self.service.device_credentials).client_id
            msg = messages.device_information('pyatv', self.srp.pairing_id.decode())
            await self.send_and_receive(msg)
            self._initial_message_sent = True
            await self.send(messages.set_ready_state())

            async def _wait_for_updates(_, semaphore):
                semaphore.release()

            semaphore = asyncio.Semaphore(value=0, loop=(self.loop))
            self.add_listener(_wait_for_updates, (protobuf.SET_STATE_MESSAGE),
              data=semaphore,
              one_shot=True)
            await self.send(messages.client_updates_config())
            await self.send(messages.wake_device())
            try:
                await asyncio.wait_for((semaphore.acquire()),
                  1, loop=(self.loop))
            except asyncio.TimeoutError:
                pass

    def stop(self):
        """Disconnect from device."""
        if self._outstanding:
            _LOGGER.warning('There were %d outstanding requests', len(self._outstanding))
        self._initial_message_sent = False
        self._outstanding = {}
        self._one_shots = {}
        self.connection.close()

    async def _connect_and_encrypt(self):
        if not self.connection.connected:
            await self.start()
        if self.service.device_credentials:
            if self._initial_message_sent:
                self._initial_message_sent = False
                credentials = Credentials.parse(self.service.device_credentials)
                pair_verifier = MrpPairingVerifier(self, self.srp, credentials)
                await pair_verifier.verify_credentials()
                output_key, input_key = pair_verifier.encryption_keys()
                self.connection.enable_encryption(output_key, input_key)

    async def send(self, message):
        """Send a message and expect no response."""
        await self._connect_and_encrypt()
        self.connection.send(message)

    async def send_and_receive(self, message, generate_identifier=True, timeout=5):
        """Send a message and wait for a response."""
        await self._connect_and_encrypt()
        if generate_identifier:
            identifier = str(uuid.uuid4())
            message.identifier = identifier
        else:
            identifier = 'type_' + str(message.type)
        self.connection.send(message)
        return await self._receive(identifier, timeout)

    async def _receive(self, identifier, timeout):
        semaphore = asyncio.Semaphore(value=0, loop=(self.loop))
        self._outstanding[identifier] = OutstandingMessage(semaphore, None)
        try:
            await asyncio.wait_for((semaphore.acquire()),
              timeout, loop=(self.loop))
        except:
            del self._outstanding[identifier]
            raise

        response = self._outstanding[identifier].response
        del self._outstanding[identifier]
        return response

    def message_received(self, message):
        """Message was received from device."""
        identifier = message.identifier or 'type_' + str(message.type)
        if identifier in self._outstanding:
            outstanding = OutstandingMessage(self._outstanding[identifier].semaphore, message)
            self._outstanding[identifier] = outstanding
            self._outstanding[identifier].semaphore.release()
        else:
            asyncio.ensure_future((self._dispatch(message)), loop=(self.loop))

    async def _dispatch(self, message):
        for listener in self._listeners.get(message.type, []):
            _LOGGER.debug('Dispatching message with type %d (%s) to %s', message.type, type(message.inner()).__name__, listener)
            await listener.func(message, listener.data)

        if message.type in self._one_shots:
            for one_shot in self._one_shots.get(message.type):
                _LOGGER.debug('One-shot with message type %d to %s', message.type, one_shot)
                await one_shot.func(message, one_shot.data)

            del self._one_shots[message.type]