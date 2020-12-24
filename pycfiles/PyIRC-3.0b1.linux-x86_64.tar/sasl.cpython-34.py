# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/sasl.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 10033 bytes
"""Identification to services.

SASL is a mechanism used by IRCv3 to authenticate clients to services in a
standard and user-friendly way. A variety of mechanisms are supported by most
servers, but only PLAIN is supported by this module at the moment.

"""
from logging import getLogger
from base64 import b64encode
from taillight.signal import SignalDefer
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)

class SASL(BaseExtension):
    __doc__ = 'The framework for SASL support. Authentication providers are needed to\n    actually provide the authentication.\n\n    :ivar mechanisms_server:\n        Mechanisms supported by the server\n\n    :ivar mechanisms:\n        Mechanisms we support as a list, which is initalised at connect time.\n\n    :ivar authenticated:\n        Whether or not we are authenticated to services\n\n    '
    requires = [
     'CapNegotiate']
    method = None

    def __init__(self, *args, **kwargs):
        """Initalise the SASL extension.

        :key sasl_mechanisms:
            An iterable of authentication providers to use, as classes. By
            default, PLAIN and EXTERNAL are used.

        """
        super().__init__(*args, **kwargs)
        self.mechanisms_server = set()
        self.username = kwargs.get('sasl_username')
        self.password = kwargs.get('sasl_password', None)
        self.authenticated = False
        self.providers = kwargs.get('sasl_mechanisms', [
         SASLPlain, SASLExternal])
        self.mechanisms = []
        self.attempt = 0

    def _create_mechanisms(self):
        """Initialise the mechanisms list."""
        self.attempt = 0
        self.mechanisms = []
        for mech in self.providers:
            provider = mech(self)
            if provider.can_authenticate:
                self.mechanisms.append(provider)
                continue

        if not self.mechanisms:
            _logger.critical('No SASL auth methods are usable!')

    @property
    def caps(self):
        """Return the SASL cap negotiation.

        :returns:
            Either "sasl" or a list of mechanisms, depending on what CAP version
            the server is using.
        """
        if not self.mechanisms:
            self._create_mechanisms()
        if not self.mechanisms:
            return
        else:
            cap_negotiate = self.base.cap_negotiate
            if 'sasl' not in cap_negotiate.remote:
                return
            if not cap_negotiate.remote['sasl']:
                _logger.debug('Registering old-style SASL capability')
                return {'sasl': []}
            _logger.debug('Registering new-style SASL capability')
            return {'sasl': [m.method for m in self.mechanisms]}

    @event('link', 'disconnected')
    def close(self, _):
        """Clean up all our state since we are disconnected now."""
        self.authenticated = False
        self.mechanisms_server.clear()
        self.mechanisms = []
        self.attempt = 0

    @event('cap_perform', 'ack', priority=100)
    def auth(self, _, line, caps):
        """Initiate authentication to the server."""
        if 'sasl' not in caps or not self.mechanisms:
            return
        cap_negotiate = self.base.cap_negotiate
        if cap_negotiate.remote['sasl']:
            params = cap_negotiate.remote['sasl']
            self.mechanisms_server = set(c.lower() for c in params)
            self.mechanisms = [m for m in self.mechanisms if m.method in params]
            if not self.mechanisms:
                _logger.critical('Server does not support any of our authentication mechanisms!')
                return
        self.send('AUTHENTICATE', [self.mechanisms[0].method])
        raise SignalDefer()

    @event('commands', Numerics.RPL_SASLSUCCESS)
    def success(self, _, line):
        """Set up state and resume the CAP event; we're authenticated!"""
        _logger.info('SASL auth succeeded as %s', self.username)
        self.authenticated = True
        if self.base.services_login:
            self.base.services_login.authenticated = True
        self.mechanisms = []
        self.attempt = 0
        return self.resume_event('cap_perform', 'ack')

    @event('commands', Numerics.ERR_SASLFAIL)
    @event('commands', Numerics.ERR_SASLABORTED)
    def fail(self, _, line):
        """Try to use the next mechanism since this one failed, or give up."""
        _logger.warning('SASL auth method %s failed as %s', self.mechanisms[self.attempt].method, self.username)
        if self.attempt + 1 >= len(self.mechanisms):
            _logger.critical('No SASL auth methods were successful.')
            return self.resume_event('cap_perform', 'ack')
        self.attempt += 1
        mechanism = self.mechanisms[self.attempt]
        self.send('AUTHENTICATE', [mechanism.method])

    @event('commands', Numerics.ERR_SASLTOOLONG)
    def fail_hard(self, _, line):
        """This is called if SASL has a hard failure (possibly due to a bug in
        the library)."""
        _logger.warning('SASL auth method %s hard failed with numeric %s', self.mechanisms[self.attempt].method, line.command)

    @event('commands', Numerics.ERR_SASLALREADY)
    def already(self, _, line):
        _logger.critical("Tried to log in twice, this shouldn't happen!")
        return self.resume_event('cap_perform', 'ack')

    @event('commands', Numerics.RPL_SASLMECHS)
    def get_mechanisms(self, _, line):
        """Retrieve the SASL mechanisms supported by the server."""
        self.mechanisms_server = set(line.params[1].lower().split(','))
        _logger.info('Supported SASL mechanisms: %r', self.mechanisms_server)

    @event('commands', 'AUTHENTICATE')
    def authenticate(self, _, line):
        """Try to authenticate with the server."""
        if self.attempt >= len(self.mechanisms):
            _logger.critical('Server requested to authenticate when we exhausted auth methods!')
            self.send('AUTHENTICATE', ['+'])
            return
        sendstr = self.mechanisms[self.attempt].authenticate(line)
        for t in (sendstr[i:i + 400] for i in range(0, len(sendstr), 400)):
            self.send('AUTHENTICATE', [t])

        if len(sendstr) % 400 == 0:
            self.send('AUTHENTICATE', ['+'])


class SASLAuthProviderBase:
    __doc__ = 'Base SASL authentication provider.'
    method = None

    def __init__(self, extension):
        self.extension = extension
        self.base = extension.base

    @property
    def can_authenticate(self):
        """Return whether or not we can authenticate."""
        raise NotImplementedError

    def authenticate(self, line):
        """Return the string to send via AUTHENTICATE."""
        raise NotImplementedError


class SASLExternal(SASLAuthProviderBase):
    __doc__ = 'EXTERNAL authentication, usually CERTFP.\n\n    .. warning::\n        This is not recommended on servers that use SHA-1 as their certificate\n        hashing mechanism (almost all), as SHA-1 is considered weak, and it is\n        possible an adversary could collide your certificate in theory.\n\n    '
    method = 'EXTERNAL'

    @property
    def can_authenticate(self):
        """Whether or not we can authenticate with this method."""
        return self.base.ssl and self.extension.password is None

    def authenticate(self, line):
        """Implement the EXTERNAL (certfp) authentication method."""
        _logger.info('Logging in with EXTERNAL method as %s', self.extension.username)
        if line.params[(-1)] != '+':
            return
        sendstr = '{0}\x00{0}\x00'.format(self.extension.username)
        sendstr = b64encode(sendstr.encode('utf-8', 'replace'))
        sendstr = sendstr.decode('utf-8')
        return sendstr


class SASLPlain(SASLAuthProviderBase):
    __doc__ = 'PLAIN authentication.\n\n    No security or encryption is performed on the string sent to the\n    server, but still suitable for use over TLS.\n\n    '
    method = 'PLAIN'

    @property
    def can_authenticate(self):
        """Whether or not we can authenticate with this method."""
        return self.extension.username and self.extension.password

    def authenticate(self, line):
        """Implement the plaintext authentication method."""
        _logger.info('Logging in with PLAIN method as %s', self.extension.username)
        if line.params[(-1)] != '+':
            return
        sendstr = '{0}\x00{0}\x00{1}'.format(self.extension.username, self.extension.password)
        sendstr = b64encode(sendstr.encode('utf-8', 'replace'))
        sendstr = sendstr.decode('utf-8')
        return sendstr