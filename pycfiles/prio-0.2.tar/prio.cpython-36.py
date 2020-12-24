# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anthony/Work/python-libprio/prio/prio.py
# Compiled at: 2018-10-22 19:27:08
# Size of source mod 2**32: 8136 bytes
from . import libprio
from array import array
PRIO_SERVER_A = libprio.PRIO_SERVER_A
PRIO_SERVER_B = libprio.PRIO_SERVER_B

class PRGSeed:

    def __init__(self):
        self.instance = libprio.PrioPRGSeed_randomize()


class Config:
    __doc__ = 'An object that stores system parameters.\n\n    The config object stores the number of data fields that are collected\n    and the modulus for modular arithmetic. The default configuration uses\n    an 87-bit modulus.\n\n    :param n_fields: The number of fields that are collected.\n    :param server_a: PublicKey of server A\n    :param server_b: PublicKey of server B\n    :param batch_id: Which batch of aggregate statistics we are computing.\n    '

    def __init__(self, n_fields, server_a, server_b, batch_id):
        self.instance = libprio.PrioConfig_new(n_fields, server_a.instance, server_b.instance, batch_id)

    def num_data_fields(self):
        return libprio.PrioConfig_numDataFields(self.instance)


class TestConfig(Config):

    def __init__(self, n_fields):
        self.instance = libprio.PrioConfig_newTest(n_fields)


class PublicKey:

    def __init__(self, instance=None):
        self.instance = instance

    def import_bin(self, data):
        """Import a curve25519 key from a raw byte string.

        :param data: a bytestring of length `CURVE25519_KEY_LEN`
        """
        self.instance = libprio.PublicKey_import(data)
        return self

    def import_hex(self, data):
        """Import a curve25519 key from a case-insenstive hex string.

        :param data: a hex bytestring of length `CURVE25519_KEY_LEN_HEX`
        """
        self.instance = libprio.PublicKey_import_hex(data)
        return self

    def export_bin(self):
        """Export a curve25519 public key as a bytestring."""
        if not self.instance:
            return
        else:
            return libprio.PublicKey_export(self.instance)

    def export_hex(self):
        """Export a curve25519 public key as a NULL-terminated hex bytestring."""
        if not self.instance:
            return
        else:
            return libprio.PublicKey_export_hex(self.instance)


class PrivateKey:

    def __init__(self, instance=None):
        self.instance = instance

    def import_bin(self, pvtdata, pubdata):
        """Import a curve25519 key from a raw byte string.

        :param pvtdata: a bytestring of length `CURVE25519_KEY_LEN`
        :param pubdata: a bytestring of length `CURVE25519_KEY_LEN`
        """
        self.instance = libprio.PrivateKey_import(pvtdata, pubdata)
        return self

    def import_hex(self, pvtdata, pubdata):
        """Import a curve25519 key from a case-insenstive hex string.

        :param pvtdata: a hex bytestring of length `CURVE25519_KEY_LEN_HEX`
        :param pubdata: a hex bytestring of length `CURVE25519_KEY_LEN_HEX`
        """
        self.instance = libprio.PrivateKey_import_hex(pvtdata, pubdata)
        return self

    def export_bin(self):
        """Export a curve25519 public key as a bytestring."""
        if not self.instance:
            return
        else:
            return libprio.PrivateKey_export(self.instance)

    def export_hex(self):
        """Export a curve25519 public key as a NULL-terminated hex bytestring."""
        if not self.instance:
            return
        else:
            return libprio.PrivateKey_export_hex(self.instance)


class Client:

    def __init__(self, config):
        self.config = config

    def encode(self, data):
        return libprio.PrioClient_encode(self.config.instance, data)


class Server:

    def __init__(self, config, server_id, private_key, secret):
        """Run the verification and aggregation routines.

        :param config: An instance of the config
        :param server_id: The enumeration of valid servers
        :param private_key: The server's private key used for decryption
        :param secret: The shared random seed
        """
        self.config = config
        self.server_id = server_id
        self.instance = libprio.PrioServer_new(config.instance, server_id, private_key.instance, secret.instance)

    def create_verifier(self, data):
        return Verifier(self, data)

    def aggregate(self, verifier):
        libprio.PrioServer_aggregate(self.instance, verifier.instance)

    def total_shares(self):
        return TotalShare(self)


class Verifier:
    __doc__ = 'The verifier is not serializable because of the reference to the\n    server. The verification packets are.\n    '

    def __init__(self, server, data):
        self.server = server
        self.instance = libprio.PrioVerifier_new(server.instance)
        libprio.PrioVerifier_set_data(self.instance, data)

    def create_verify1(self):
        return PacketVerify1(self)

    def create_verify2(self, verify1A, verify1B):
        verify1A.deserialize(self.server.config)
        verify1B.deserialize(self.server.config)
        return PacketVerify2(self, verify1A, verify1B)

    def is_valid(self, verify2A, verify2B):
        verify2A.deserialize(self.server.config)
        verify2B.deserialize(self.server.config)
        try:
            libprio.PrioVerifier_isValid(self.instance, verify2A.instance, verify2B.instance)
            return True
        except RuntimeError:
            return False


class PacketVerify1:

    def __init__(self, verifier):
        self.instance = libprio.PrioPacketVerify1_new()
        libprio.PrioPacketVerify1_set_data(self.instance, verifier.instance)
        self._serial_data = None

    def deserialize(self, config):
        if self._serial_data:
            libprio.PrioPacketVerify1_read(self.instance, self._serial_data, config.instance)
        self._serial_data = None

    def __getstate__(self):
        return libprio.PrioPacketVerify1_write(self.instance)

    def __setstate__(self, state):
        self.instance = libprio.PrioPacketVerify1_new()
        self._serial_data = state


class PacketVerify2:

    def __init__(self, verifier, A, B):
        self.instance = libprio.PrioPacketVerify2_new()
        libprio.PrioPacketVerify2_set_data(self.instance, verifier.instance, A.instance, B.instance)
        self._serial_data = None

    def deserialize(self, config):
        if self._serial_data:
            libprio.PrioPacketVerify2_read(self.instance, self._serial_data, config.instance)
        self._serial_data = None

    def __getstate__(self):
        return libprio.PrioPacketVerify2_write(self.instance)

    def __setstate__(self, state):
        self.instance = libprio.PrioPacketVerify2_new()
        self._serial_data = state


class TotalShare:

    def __init__(self, server):
        self.instance = libprio.PrioTotalShare_new()
        libprio.PrioTotalShare_set_data(self.instance, server.instance)
        self._serial_data = None

    def deserialize(self, config):
        if self._serial_data:
            libprio.PrioTotalShare_read(self.instance, self._serial_data, config.instance)
        self._serial_data = None

    def __getstate__(self):
        return libprio.PrioTotalShare_write(self.instance)

    def __setstate__(self, state):
        self.instance = libprio.PrioTotalShare_new()
        self._serial_data = state


def create_keypair():
    secret, public = libprio.Keypair_new()
    return (PrivateKey(secret), PublicKey(public))


def total_share_final(config, tA, tB):
    tA.deserialize(config)
    tB.deserialize(config)
    final = libprio.PrioTotalShare_final(config.instance, tA.instance, tB.instance)
    return array('L', final)