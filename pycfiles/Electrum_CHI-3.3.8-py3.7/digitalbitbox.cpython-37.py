# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/digitalbitbox/digitalbitbox.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 32370 bytes
import base64, binascii, hashlib, hmac, json, math, os, re, struct, sys, time
from electrum.crypto import sha256d, EncodeAES_base64, EncodeAES_bytes, DecodeAES_bytes, hmac_oneshot
from electrum.bitcoin import TYPE_ADDRESS, push_script, var_int, public_key_to_p2pkh, is_address
from electrum.bip32 import BIP32Node
from electrum import ecc
from electrum.ecc import msg_magic
from electrum.wallet import Standard_Wallet
from electrum import constants
from electrum.transaction import Transaction
from electrum.i18n import _
from electrum.keystore import Hardware_KeyStore
from ..hw_wallet import HW_PluginBase
from electrum.util import to_string, UserCancelled, UserFacingException
from electrum.base_wizard import ScriptTypeNotSupported, HWD_SETUP_NEW_WALLET
from electrum.network import Network
from electrum.logging import get_logger
_logger = get_logger(__name__)
try:
    import hid
    DIGIBOX = True
except ImportError as e:
    try:
        DIGIBOX = False
    finally:
        e = None
        del e

def to_hexstr(s):
    return binascii.hexlify(s).decode('ascii')


def derive_keys(x):
    h = sha256d(x)
    h = hashlib.sha512(h).digest()
    return (h[:32], h[32:])


MIN_MAJOR_VERSION = 5
ENCRYPTION_PRIVKEY_KEY = 'encryptionprivkey'
CHANNEL_ID_KEY = 'comserverchannelid'

class DigitalBitbox_Client:

    def __init__(self, plugin, hidDevice):
        self.plugin = plugin
        self.dbb_hid = hidDevice
        self.opened = True
        self.password = None
        self.isInitialized = False
        self.setupRunning = False
        self.usbReportSize = 64

    def close(self):
        if self.opened:
            try:
                self.dbb_hid.close()
            except:
                pass

        self.opened = False

    def timeout(self, cutoff):
        pass

    def label(self):
        return ' '

    def is_pairable(self):
        return True

    def is_initialized(self):
        return self.dbb_has_password()

    def is_paired(self):
        return self.password is not None

    def has_usable_connection_with_device(self):
        try:
            self.dbb_has_password()
        except BaseException:
            return False
        else:
            return True

    def _get_xpub(self, bip32_path):
        if self.check_device_dialog():
            return self.hid_send_encrypt(('{"xpub": "%s"}' % bip32_path).encode('utf8'))

    def get_xpub(self, bip32_path, xtype):
        assert xtype in self.plugin.SUPPORTED_XTYPES
        reply = self._get_xpub(bip32_path)
        if reply:
            xpub = reply['xpub']
            if xtype != 'standard' or constants.net.TESTNET:
                node = BIP32Node.from_xkey(xpub, net=(constants.BitcoinMainnet))
                xpub = node._replace(xtype=xtype).to_xpub()
            return xpub
        raise Exception('no reply')

    def dbb_has_password(self):
        reply = self.hid_send_plain(b'{"ping":""}')
        if 'ping' not in reply:
            raise UserFacingException(_('Device communication error. Please unplug and replug your Digital Bitbox.'))
        if reply['ping'] == 'password':
            return True
        return False

    def stretch_key(self, key: bytes):
        return to_hexstr(hashlib.pbkdf2_hmac('sha512', key, b'Digital Bitbox', iterations=20480))

    def backup_password_dialog(self):
        msg = _('Enter the password used when the backup was created:')
        while True:
            password = self.handler.get_passphrase(msg, False)
            if password is None:
                return
            if len(password) < 4:
                msg = _('Password must have at least 4 characters.') + '\n\n' + _('Enter password:')
            elif len(password) > 64:
                msg = _('Password must have less than 64 characters.') + '\n\n' + _('Enter password:')
            else:
                return password.encode('utf8')

    def password_dialog(self, msg):
        while True:
            password = self.handler.get_passphrase(msg, False)
            if password is None:
                return False
            if len(password) < 4:
                msg = _('Password must have at least 4 characters.') + '\n\n' + _('Enter password:')
            elif len(password) > 64:
                msg = _('Password must have less than 64 characters.') + '\n\n' + _('Enter password:')
            else:
                self.password = password.encode('utf8')
                return True

    def check_device_dialog(self):
        match = re.search('v([0-9])+\\.[0-9]+\\.[0-9]+', self.dbb_hid.get_serial_number_string())
        if match is None:
            raise Exception('error detecting firmware version')
        else:
            major_version = int(match.group(1))
            if major_version < MIN_MAJOR_VERSION:
                raise Exception('Please upgrade to the newest firmware using the BitBox Desktop app: https://shiftcrypto.ch/start')
            if self.password is None:
                if not self.dbb_has_password():
                    if not self.setupRunning:
                        return False
                        msg = _('An uninitialized Digital Bitbox is detected.') + ' ' + _('Enter a new password below.') + '\n\n' + _('REMEMBER THE PASSWORD!') + '\n\n' + _('You cannot access your coins or a backup without the password.') + '\n' + _('A backup is saved automatically when generating a new wallet.')
                        if self.password_dialog(msg):
                            reply = self.hid_send_plain(b'{"password":"' + self.password + b'"}')
                    else:
                        return False
        msg = _('Enter your Digital Bitbox password:')
        while self.password is None:
            if not self.password_dialog(msg):
                raise UserCancelled()
            reply = self.hid_send_encrypt(b'{"led":"blink"}')
            if 'error' in reply:
                self.password = None
                if reply['error']['code'] == 109:
                    msg = _('Incorrect password entered.') + '\n\n' + reply['error']['message'] + '\n\n' + _('Enter your Digital Bitbox password:')
                else:
                    msg = _('Unexpected error occurred.') + '\n\n' + reply['error']['message'] + '\n\n' + _('Enter your Digital Bitbox password:')

        if not self.setupRunning:
            self.isInitialized = True
        else:
            if not self.isInitialized:
                reply = self.hid_send_encrypt(b'{"device":"info"}')
                if reply['device']['id'] != '':
                    self.recover_or_erase_dialog()
                else:
                    self.seed_device_dialog()
                self.mobile_pairing_dialog()
            return self.isInitialized

    def recover_or_erase_dialog(self):
        msg = _('The Digital Bitbox is already seeded. Choose an option:') + '\n'
        choices = [
         _('Create a wallet using the current seed'),
         _('Load a wallet from the micro SD card (the current seed is overwritten)'),
         _('Erase the Digital Bitbox')]
        try:
            reply = self.handler.win.query_choice(msg, choices)
        except Exception:
            return
        else:
            if reply == 2:
                self.dbb_erase()
            else:
                if reply == 1:
                    return self.dbb_load_backup() or None
                else:
                    if self.hid_send_encrypt(b'{"device":"info"}')['device']['lock']:
                        raise UserFacingException(_('Full 2FA enabled. This is not supported yet.'))
            self.isInitialized = True

    def seed_device_dialog(self):
        msg = _('Choose how to initialize your Digital Bitbox:') + '\n'
        choices = [
         _('Generate a new random wallet'),
         _('Load a wallet from the micro SD card')]
        try:
            reply = self.handler.win.query_choice(msg, choices)
        except Exception:
            return
        else:
            if reply == 0:
                self.dbb_generate_wallet()
            else:
                if not self.dbb_load_backup(show_msg=False):
                    return
            self.isInitialized = True

    def mobile_pairing_dialog(self):
        dbb_user_dir = None
        if sys.platform == 'darwin':
            dbb_user_dir = os.path.join(os.environ.get('HOME', ''), 'Library', 'Application Support', 'DBB')
        else:
            if sys.platform == 'win32':
                dbb_user_dir = os.path.join(os.environ['APPDATA'], 'DBB')
            else:
                dbb_user_dir = os.path.join(os.environ['HOME'], '.dbb')
        if not dbb_user_dir:
            return
            try:
                jsonDecodeError = json.JSONDecodeError
            except AttributeError:
                jsonDecodeError = ValueError

            try:
                with open(os.path.join(dbb_user_dir, 'config.dat')) as (f):
                    dbb_config = json.load(f)
            except (FileNotFoundError, jsonDecodeError):
                return
            else:
                if ENCRYPTION_PRIVKEY_KEY not in dbb_config or CHANNEL_ID_KEY not in dbb_config:
                    return
                choices = [_('Do not pair'),
                 _('Import pairing from the Digital Bitbox desktop app')]
                try:
                    reply = self.handler.win.query_choice(_('Mobile pairing options'), choices)
                except Exception:
                    return
                else:
                    if reply == 0:
                        if self.plugin.is_mobile_paired():
                            del self.plugin.digitalbitbox_config[ENCRYPTION_PRIVKEY_KEY]
                            del self.plugin.digitalbitbox_config[CHANNEL_ID_KEY]
        else:
            if reply == 1:
                self.plugin.digitalbitbox_config[ENCRYPTION_PRIVKEY_KEY] = dbb_config[ENCRYPTION_PRIVKEY_KEY]
                self.plugin.digitalbitbox_config[CHANNEL_ID_KEY] = dbb_config[CHANNEL_ID_KEY]
            self.plugin.config.set_key('digitalbitbox', self.plugin.digitalbitbox_config)

    def dbb_generate_wallet(self):
        key = self.stretch_key(self.password)
        filename = 'Electrum-' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.pdf'
        msg = ('{"seed":{"source": "create", "key": "%s", "filename": "%s", "entropy": "%s"}}' % (key, filename, to_hexstr(os.urandom(32)))).encode('utf8')
        reply = self.hid_send_encrypt(msg)
        if 'error' in reply:
            raise UserFacingException(reply['error']['message'])

    def dbb_erase(self):
        self.handler.show_message(_('Are you sure you want to erase the Digital Bitbox?') + '\n\n' + _("To continue, touch the Digital Bitbox's light for 3 seconds.") + '\n\n' + _('To cancel, briefly touch the light or wait for the timeout.'))
        hid_reply = self.hid_send_encrypt(b'{"reset":"__ERASE__"}')
        self.handler.finished()
        if 'error' in hid_reply:
            raise UserFacingException(hid_reply['error']['message'])
        else:
            self.password = None
            raise UserFacingException('Device erased')

    def dbb_load_backup(self, show_msg=True):
        backups = self.hid_send_encrypt(b'{"backup":"list"}')
        if 'error' in backups:
            raise UserFacingException(backups['error']['message'])
        try:
            f = self.handler.win.query_choice(_('Choose a backup file:'), backups['backup'])
        except Exception:
            return False
        else:
            key = self.backup_password_dialog()
            if key is None:
                raise Exception('Canceled by user')
            key = self.stretch_key(key)
            if show_msg:
                self.handler.show_message(_('Loading backup...') + '\n\n' + _("To continue, touch the Digital Bitbox's light for 3 seconds.") + '\n\n' + _('To cancel, briefly touch the light or wait for the timeout.'))
            msg = ('{"seed":{"source": "backup", "key": "%s", "filename": "%s"}}' % (key, backups['backup'][f])).encode('utf8')
            hid_reply = self.hid_send_encrypt(msg)
            self.handler.finished()
            if 'error' in hid_reply:
                raise UserFacingException(hid_reply['error']['message'])
            return True

    def hid_send_frame(self, data):
        HWW_CID = 4278190080
        HWW_CMD = 193
        data_len = len(data)
        seq = 0
        idx = 0
        write = []
        while idx < data_len:
            if idx == 0:
                write = data[idx:idx + min(data_len, self.usbReportSize - 7)]
                self.dbb_hid.write(b'\x00' + struct.pack('>IBH', HWW_CID, HWW_CMD, data_len & 65535) + write + b'\xee' * (self.usbReportSize - 7 - len(write)))
            else:
                write = data[idx:idx + min(data_len, self.usbReportSize - 5)]
                self.dbb_hid.write(b'\x00' + struct.pack('>IB', HWW_CID, seq) + write + b'\xee' * (self.usbReportSize - 5 - len(write)))
                seq += 1
            idx += len(write)

    def hid_read_frame(self):
        read = bytearray(self.dbb_hid.read(self.usbReportSize))
        cid = ((read[0] * 256 + read[1]) * 256 + read[2]) * 256 + read[3]
        cmd = read[4]
        data_len = read[5] * 256 + read[6]
        data = read[7:]
        idx = len(read) - 7
        while idx < data_len:
            read = bytearray(self.dbb_hid.read(self.usbReportSize))
            data += read[5:]
            idx += len(read) - 5

        return data

    def hid_send_plain(self, msg):
        reply = ''
        try:
            serial_number = self.dbb_hid.get_serial_number_string()
            if 'v2.0.' in serial_number or 'v1.' in serial_number:
                hidBufSize = 4096
                self.dbb_hid.write('\x00' + msg + '\x00' * (hidBufSize - len(msg)))
                r = bytearray()
                while len(r) < hidBufSize:
                    r += bytearray(self.dbb_hid.read(hidBufSize))

            else:
                self.hid_send_frame(msg)
                r = self.hid_read_frame()
            r = r.rstrip(b' \t\r\n\x00')
            r = r.replace(b'\x00', b'')
            r = to_string(r, 'utf8')
            reply = json.loads(r)
        except Exception as e:
            try:
                _logger.info(f"Exception caught {repr(e)}")
            finally:
                e = None
                del e

        return reply

    def hid_send_encrypt(self, msg):
        sha256_byte_len = 32
        reply = ''
        try:
            encryption_key, authentication_key = derive_keys(self.password)
            msg = EncodeAES_bytes(encryption_key, msg)
            hmac_digest = hmac_oneshot(authentication_key, msg, hashlib.sha256)
            authenticated_msg = base64.b64encode(msg + hmac_digest)
            reply = self.hid_send_plain(authenticated_msg)
            if 'ciphertext' in reply:
                b64_unencoded = bytes(base64.b64decode(''.join(reply['ciphertext'])))
                reply_hmac = b64_unencoded[-sha256_byte_len:]
                hmac_calculated = hmac_oneshot(authentication_key, b64_unencoded[:-sha256_byte_len], hashlib.sha256)
                if not hmac.compare_digest(reply_hmac, hmac_calculated):
                    raise Exception('Failed to validate HMAC')
                reply = DecodeAES_bytes(encryption_key, b64_unencoded[:-sha256_byte_len])
                reply = to_string(reply, 'utf8')
                reply = json.loads(reply)
            if 'error' in reply:
                self.password = None
        except Exception as e:
            try:
                _logger.info(f"Exception caught {repr(e)}")
            finally:
                e = None
                del e

        return reply


class DigitalBitbox_KeyStore(Hardware_KeyStore):
    hw_type = 'digitalbitbox'
    device = 'DigitalBitbox'

    def __init__(self, d):
        Hardware_KeyStore.__init__(self, d)
        self.force_watching_only = False
        self.maxInputs = 14

    def get_derivation(self):
        return str(self.derivation)

    def is_p2pkh(self):
        return self.derivation.startswith("m/44'/")

    def give_error(self, message, clear_client=False):
        if clear_client:
            self.client = None
        raise Exception(message)

    def decrypt_message(self, pubkey, message, password):
        raise RuntimeError(_('Encryption and decryption are currently not supported for {}').format(self.device))

    def sign_message(self, sequence, message, password):
        sig = None
        try:
            message = message.encode('utf8')
            inputPath = self.get_derivation() + '/%d/%d' % sequence
            msg_hash = sha256d(msg_magic(message))
            inputHash = to_hexstr(msg_hash)
            hasharray = []
            hasharray.append({'hash':inputHash,  'keypath':inputPath})
            hasharray = json.dumps(hasharray)
            msg = ('{"sign":{"meta":"sign message", "data":%s}}' % hasharray).encode('utf8')
            dbb_client = self.plugin.get_client(self)
            if not dbb_client.is_paired():
                raise Exception(_('Could not sign message.'))
            else:
                reply = dbb_client.hid_send_encrypt(msg)
                self.handler.show_message(_('Signing message ...') + '\n\n' + _("To continue, touch the Digital Bitbox's blinking light for 3 seconds.") + '\n\n' + _('To cancel, briefly touch the blinking light or wait for the timeout.'))
                reply = dbb_client.hid_send_encrypt(msg)
                self.handler.finished()
                if 'error' in reply:
                    raise Exception(reply['error']['message'])
                else:
                    if 'sign' not in reply:
                        raise Exception(_('Could not sign message.'))
                    if 'recid' in reply['sign'][0]:
                        sig_string = binascii.unhexlify(reply['sign'][0]['sig'])
                        recid = int(reply['sign'][0]['recid'], 16)
                        sig = ecc.construct_sig65(sig_string, recid, True)
                        pubkey, compressed = ecc.ECPubkey.from_signature65(sig, msg_hash)
                        addr = public_key_to_p2pkh(pubkey.get_public_key_bytes(compressed=compressed))
                        if ecc.verify_message_with_address(addr, sig, message) is False:
                            raise Exception(_('Could not sign message'))
                    elif 'pubkey' in reply['sign'][0]:
                        for recid in range(4):
                            sig_string = binascii.unhexlify(reply['sign'][0]['sig'])
                            sig = ecc.construct_sig65(sig_string, recid, True)
                            try:
                                addr = public_key_to_p2pkh(binascii.unhexlify(reply['sign'][0]['pubkey']))
                                if ecc.verify_message_with_address(addr, sig, message):
                                    break
                            except Exception:
                                continue

                        else:
                            raise Exception(_('Could not sign message'))

        except BaseException as e:
            try:
                self.give_error(e)
            finally:
                e = None
                del e

        return sig

    def sign_transaction(self, tx, password):
        if tx.is_complete():
            return
        try:
            p2pkhTransaction = True
            derivations = self.get_tx_derivations(tx)
            inputhasharray = []
            hasharray = []
            pubkeyarray = []
            for i, txin in enumerate(tx.inputs()):
                if txin['type'] == 'coinbase':
                    self.give_error('Coinbase not supported')
                if txin['type'] != 'p2pkh':
                    p2pkhTransaction = False
                for x_pubkey in txin['x_pubkeys']:
                    if x_pubkey in derivations:
                        index = derivations.get(x_pubkey)
                        inputPath = '%s/%d/%d' % (self.get_derivation(), index[0], index[1])
                        inputHash = sha256d(binascii.unhexlify(tx.serialize_preimage(i)))
                        hasharray_i = {'hash':to_hexstr(inputHash),  'keypath':inputPath}
                        hasharray.append(hasharray_i)
                        inputhasharray.append(inputHash)
                        break
                else:
                    self.give_error('No matching x_key for sign_transaction')

            for o in tx.outputs():
                assert o.type == TYPE_ADDRESS
                info = tx.output_info.get(o.address)
                if info is not None:
                    index = info.address_index
                    changePath = self.get_derivation() + '/%d/%d' % index
                    changePubkey = self.derive_pubkey(index[0], index[1])
                    pubkeyarray_i = {'pubkey':changePubkey,  'keypath':changePath}
                    pubkeyarray.append(pubkeyarray_i)

            if p2pkhTransaction:

                class CustomTXSerialization(Transaction):

                    @classmethod
                    def input_script(self, txin, estimate_size=False):
                        if txin['type'] == 'p2pkh':
                            return Transaction.get_preimage_script(txin)
                        if txin['type'] == 'p2sh':
                            return '00' + push_script(Transaction.get_preimage_script(txin))
                        raise Exception('unsupported type %s' % txin['type'])

                tx_dbb_serialized = CustomTXSerialization(tx.serialize()).serialize_to_network()
            else:
                tx_dbb_serialized = None
            dbb_signatures = []
            steps = math.ceil(1.0 * len(hasharray) / self.maxInputs)
            for step in range(int(steps)):
                hashes = hasharray[step * self.maxInputs:(step + 1) * self.maxInputs]
                msg = {'sign': {'data':hashes, 
                          'checkpub':pubkeyarray}}
                if tx_dbb_serialized is not None:
                    msg['sign']['meta'] = to_hexstr(sha256d(tx_dbb_serialized))
                msg = json.dumps(msg).encode('ascii')
                dbb_client = self.plugin.get_client(self)
                if not dbb_client.is_paired():
                    raise Exception('Could not sign transaction.')
                reply = dbb_client.hid_send_encrypt(msg)
                if 'error' in reply:
                    raise Exception(reply['error']['message'])
                if 'echo' not in reply:
                    raise Exception('Could not sign transaction.')
                elif self.plugin.is_mobile_paired():
                    if tx_dbb_serialized is not None:
                        reply['tx'] = tx_dbb_serialized
                        self.plugin.comserver_post_notification(reply)
                    if steps > 1:
                        self.handler.show_message(_('Signing large transaction. Please be patient ...') + '\n\n' + _("To continue, touch the Digital Bitbox's blinking light for 3 seconds.") + ' ' + _('(Touch {} of {})').format(step + 1, steps) + '\n\n' + _('To cancel, briefly touch the blinking light or wait for the timeout.') + '\n\n')
                else:
                    self.handler.show_message(_('Signing transaction...') + '\n\n' + _("To continue, touch the Digital Bitbox's blinking light for 3 seconds.") + '\n\n' + _('To cancel, briefly touch the blinking light or wait for the timeout.'))
                reply = dbb_client.hid_send_encrypt(msg)
                self.handler.finished()
                if 'error' in reply:
                    if reply['error'].get('code') in (600, 601):
                        raise UserCancelled()
                    raise Exception(reply['error']['message'])
                if 'sign' not in reply:
                    raise Exception('Could not sign transaction.')
                dbb_signatures.extend(reply['sign'])

            if len(dbb_signatures) != len(tx.inputs()):
                raise Exception('Incorrect number of transactions signed.')
            for i, txin in enumerate(tx.inputs()):
                num = txin['num_sig']
                for pubkey in txin['pubkeys']:
                    signatures = list(filter(None, txin['signatures']))
                    if len(signatures) == num:
                        break
                    ii = txin['pubkeys'].index(pubkey)
                    signed = dbb_signatures[i]
                    if 'recid' in signed:
                        recid = int(signed['recid'], 16)
                        s = binascii.unhexlify(signed['sig'])
                        h = inputhasharray[i]
                        pk = ecc.ECPubkey.from_sig_string(s, recid, h)
                        pk = pk.get_public_key_hex(compressed=True)
                    else:
                        if 'pubkey' in signed:
                            pk = signed['pubkey']
                        if pk != pubkey:
                            continue
                        sig_r = int(signed['sig'][:64], 16)
                        sig_s = int(signed['sig'][64:], 16)
                        sig = ecc.der_sig_from_r_and_s(sig_r, sig_s)
                        sig = to_hexstr(sig) + '01'
                        tx.add_signature_to_txin(i, ii, sig)

        except UserCancelled:
            raise
        except BaseException as e:
            try:
                self.give_error(e, True)
            finally:
                e = None
                del e

        else:
            _logger.info('Transaction is_complete {tx.is_complete()}')
            tx.raw = tx.serialize()


class DigitalBitboxPlugin(HW_PluginBase):
    libraries_available = DIGIBOX
    keystore_class = DigitalBitbox_KeyStore
    client = None
    DEVICE_IDS = [
     (1003, 9218)]
    SUPPORTED_XTYPES = ('standard', 'p2wpkh-p2sh', 'p2wpkh', 'p2wsh-p2sh', 'p2wsh')

    def __init__(self, parent, config, name):
        HW_PluginBase.__init__(self, parent, config, name)
        if self.libraries_available:
            self.device_manager().register_devices(self.DEVICE_IDS)
        self.digitalbitbox_config = self.config.get('digitalbitbox', {})

    def get_dbb_device(self, device):
        dev = hid.device()
        dev.open_path(device.path)
        return dev

    def create_client(self, device, handler):
        if device.interface_number == 0 or device.usage_page == 65535:
            if handler:
                self.handler = handler
            client = self.get_dbb_device(device)
            if client is not None:
                client = DigitalBitbox_Client(self, client)
            return client
        return

    def setup_device(self, device_info, wizard, purpose):
        devmgr = self.device_manager()
        device_id = device_info.device.id_
        client = devmgr.client_by_id(device_id)
        if client is None:
            raise Exception(_('Failed to create a client for this device.') + '\n' + _('Make sure it is in the correct state.'))
        client.handler = self.create_handler(wizard)
        if purpose == HWD_SETUP_NEW_WALLET:
            client.setupRunning = True
        client.get_xpub("m/44'/0'", 'standard')

    def is_mobile_paired(self):
        return ENCRYPTION_PRIVKEY_KEY in self.digitalbitbox_config

    def comserver_post_notification(self, payload):
        assert self.is_mobile_paired(), 'unexpected mobile pairing error'
        url = 'https://digitalbitbox.com/smartverification/index.php'
        key_s = base64.b64decode(self.digitalbitbox_config[ENCRYPTION_PRIVKEY_KEY])
        args = 'c=data&s=0&dt=0&uuid=%s&pl=%s' % (
         self.digitalbitbox_config[CHANNEL_ID_KEY],
         EncodeAES_base64(key_s, json.dumps(payload).encode('ascii')).decode('ascii'))
        try:
            text = Network.send_http_on_proxy('post', url, body=(args.encode('ascii')), headers={'content-type': 'application/x-www-form-urlencoded'})
            _logger.info(f"digitalbitbox reply from server {text}")
        except Exception as e:
            try:
                self.handler.show_error(repr(e))
            finally:
                e = None
                del e

    def get_xpub(self, device_id, derivation, xtype, wizard):
        if xtype not in self.SUPPORTED_XTYPES:
            raise ScriptTypeNotSupported(_('This type of script is not supported with {}.').format(self.device))
        devmgr = self.device_manager()
        client = devmgr.client_by_id(device_id)
        client.handler = self.create_handler(wizard)
        client.check_device_dialog()
        xpub = client.get_xpub(derivation, xtype)
        return xpub

    def get_client(self, keystore, force_pair=True):
        devmgr = self.device_manager()
        handler = keystore.handler
        with devmgr.hid_lock:
            client = devmgr.client_for_keystore(self, handler, keystore, force_pair)
        if client is not None:
            client.check_device_dialog()
        return client

    def show_address(self, wallet, address, keystore=None):
        if keystore is None:
            keystore = wallet.get_keystore()
        else:
            if not self.show_address_helper(wallet, address, keystore):
                return
            else:
                if type(wallet) is not Standard_Wallet:
                    keystore.handler.show_error(_('This function is only available for standard wallets when using {}.').format(self.device))
                    return
                self.is_mobile_paired() or keystore.handler.show_error(_('This function is only available after pairing your {} with a mobile device.').format(self.device))
                return
            keystore.is_p2pkh() or keystore.handler.show_error(_('This function is only available for p2pkh keystores when using {}.').format(self.device))
            return
        change, index = wallet.get_address_index(address)
        keypath = '%s/%d/%d' % (keystore.derivation, change, index)
        xpub = self.get_client(keystore)._get_xpub(keypath)
        verify_request_payload = {'type':'p2pkh', 
         'echo':xpub['echo']}
        self.comserver_post_notification(verify_request_payload)