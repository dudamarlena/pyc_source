# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/airplay/api.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 2454 bytes
"""Implementation of external API for AirPlay."""
import logging, binascii
from pyatv.interface import AirPlay
from pyatv.airplay.srp import SRPAuthHandler, new_credentials
from pyatv.airplay.auth import AuthenticationVerifier, DeviceAuthenticator
_LOGGER = logging.getLogger(__name__)

class AirPlayAPI(AirPlay):
    __doc__ = 'Implementation of API for AirPlay support.'

    def __init__(self, http, airplay_player):
        """Initialize a new AirPlayInternal instance."""
        self.player = airplay_player
        self.identifier = None
        self.srp = SRPAuthHandler()
        self.verifier = AuthenticationVerifier(http, self.srp)
        self.auther = DeviceAuthenticator(http, self.srp)

    async def generate_credentials(self):
        """Create new credentials for authentication.

        Credentials that have been authenticated shall be saved and loaded with
        load_credentials before playing anything. If credentials are lost,
        authentication must be performed again.
        """
        identifier, seed = new_credentials()
        return '{0}:{1}'.format(identifier, seed.decode().upper())

    async def load_credentials(self, credentials):
        """Load existing credentials."""
        split = credentials.split(':')
        self.identifier = split[0]
        self.srp.initialize(binascii.unhexlify(split[1]))
        _LOGGER.debug('Loaded AirPlay credentials: %s', credentials)

    def verify_authenticated(self):
        """Check if loaded credentials are verified."""
        return self.verifier.verify_authed()

    def start_authentication(self):
        """Begin authentication proces (show PIN on screen)."""
        return self.auther.start_authentication()

    def finish_authentication(self, pin):
        """End authentication process with PIN code."""
        return self.auther.finish_authentication(self.identifier, pin)

    async def play_url(self, url, **kwargs):
        """Play media from an URL on the device.

        Note: This method will not yield until the media has finished playing.
        The Apple TV requires the request to stay open during the entire
        play duration.
        """
        if self.identifier:
            await self.verify_authenticated()
        position = 0 if 'position' not in kwargs else int(kwargs['position'])
        return await self.player.play_url(url, position)