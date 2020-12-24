# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/coldcard/coldcard.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 26391 bytes
from struct import pack, unpack
import os, sys, time, io, traceback
from electrum.bip32 import BIP32Node, InvalidMasterKeyVersionBytes
from electrum.i18n import _
from electrum.plugin import Device
from electrum.keystore import Hardware_KeyStore, xpubkey_to_pubkey, Xpub
from electrum.transaction import Transaction
from electrum.wallet import Standard_Wallet
from electrum.crypto import hash_160
from electrum.util import bfh, bh2u, versiontuple, UserFacingException
from electrum.base_wizard import ScriptTypeNotSupported
from electrum.logging import get_logger
from ..hw_wallet import HW_PluginBase
from hw_wallet.plugin import LibraryFoundButUnusable
_logger = get_logger(__name__)
try:
    import hid
    from ckcc.protocol import CCProtocolPacker, CCProtocolUnpacker
    from ckcc.protocol import CCProtoError, CCUserRefused, CCBusyError
    from ckcc.constants import MAX_MSG_LEN, MAX_BLK_LEN, MSG_SIGNING_MAX_LENGTH, MAX_TXN_LEN, AF_CLASSIC, AF_P2SH, AF_P2WPKH, AF_P2WSH, AF_P2WPKH_P2SH, AF_P2WSH_P2SH
    from ckcc.constants import PSBT_GLOBAL_UNSIGNED_TX, PSBT_IN_NON_WITNESS_UTXO, PSBT_IN_WITNESS_UTXO, PSBT_IN_SIGHASH_TYPE, PSBT_IN_REDEEM_SCRIPT, PSBT_IN_WITNESS_SCRIPT, PSBT_IN_BIP32_DERIVATION, PSBT_OUT_BIP32_DERIVATION, PSBT_OUT_REDEEM_SCRIPT
    from ckcc.client import ColdcardDevice, COINKITE_VID, CKCC_PID, CKCC_SIMULATOR_PATH
    requirements_ok = True

    class ElectrumColdcardDevice(ColdcardDevice):

        def mitm_verify(self, sig, expect_xpub):
            pubkey = BIP32Node.from_xkey(expect_xpub).eckey
            try:
                pubkey.verify_message_hash(sig[1:65], self.session_key)
                return True
            except:
                return False


except ImportError:
    requirements_ok = False
    COINKITE_VID = 53566
    CKCC_PID = 52240

CKCC_SIMULATED_PID = CKCC_PID ^ 21930

def my_var_int(l):
    if l < 253:
        return pack('B', l)
    if l < 65536:
        return pack('<BH', 253, l)
    if l < 4294967296:
        return pack('<BI', 254, l)
    return pack('<BQ', 255, l)


def xfp_from_xpub(xpub):
    kk = bfh(Xpub.get_pubkey_from_xpub(xpub, []))
    assert len(kk) == 33
    xfp, = unpack('<I', hash_160(kk)[0:4])
    return xfp


class CKCCClient:

    def __init__(self, plugin, handler, dev_path, is_simulator=False):
        self.device = plugin.device
        self.handler = handler
        self._expected_device = None
        if is_simulator:
            self.dev = ElectrumColdcardDevice(dev_path, encrypt=True)
        else:
            import hid
            hd = hid.device(path=dev_path)
            hd.open_path(dev_path)
            self.dev = ElectrumColdcardDevice(dev=hd, encrypt=True)

    def __repr__(self):
        return '<CKCCClient: xfp=%08x label=%r>' % (self.dev.master_fingerprint,
         self.label())

    def verify_connection(self, expected_xfp, expected_xpub):
        ex = (
         expected_xfp, expected_xpub)
        if self._expected_device == ex:
            return
        if self._expected_device is not None or self.dev.master_fingerprint != expected_xfp or self.dev.master_xpub != expected_xpub:
            _logger.info(f"xpubs. reported by device: {self.dev.master_xpub}. stored in file: {expected_xpub}")
            raise RuntimeError("Expecting 0x%08x but that's not what's connected?!" % expected_xfp)
        self.dev.check_mitm(expected_xpub=expected_xpub)
        self._expected_device = ex
        _logger.info('Successfully verified against MiTM')

    def is_pairable(self):
        return bool(self.dev.master_xpub)

    def timeout(self, cutoff):
        pass

    def close(self):
        self.dev.close()
        self.dev = None

    def is_initialized(self):
        return bool(self.dev.master_xpub)

    def label(self):
        if self.dev.is_simulator:
            lab = 'Coldcard Simulator 0x%08x' % self.dev.master_fingerprint
        else:
            if not self.dev.master_fingerprint:
                lab = 'Coldcard #' + self.dev.serial
            else:
                lab = 'Coldcard 0x%08x' % self.dev.master_fingerprint

        class LabelStr(str):

            def __new__(cls, s, xfp=None, xpub=None):
                self = super().__new__(cls, str(s))
                self.xfp = getattr(s, 'xfp', xfp)
                self.xpub = getattr(s, 'xpub', xpub)
                return self

        return LabelStr(lab, self.dev.master_fingerprint, self.dev.master_xpub)

    def has_usable_connection_with_device(self):
        try:
            self.ping_check()
            return True
        except:
            return False

    def get_xpub(self, bip32_path, xtype):
        assert xtype in ColdcardPlugin.SUPPORTED_XTYPES
        _logger.info('Derive xtype = %r' % xtype)
        xpub = self.dev.send_recv((CCProtocolPacker.get_xpub(bip32_path)), timeout=5000)
        try:
            node = BIP32Node.from_xkey(xpub)
        except InvalidMasterKeyVersionBytes:
            raise UserFacingException(_('Invalid xpub magic. Make sure your {} device is set to the correct chain.').format(self.device)) from None

        if xtype != 'standard':
            xpub = node._replace(xtype=xtype).to_xpub()
        return xpub

    def ping_check(self):
        assert self.dev.session_key, 'not encrypted?'
        req = b'1234 Electrum Plugin 4321'
        try:
            echo = self.dev.send_recv(CCProtocolPacker.ping(req))
            assert echo == req
        except:
            raise RuntimeError('Communication trouble with Coldcard')

    def show_address(self, path, addr_fmt):
        return self.dev.send_recv((CCProtocolPacker.show_address(path, addr_fmt)), timeout=None)

    def get_version(self):
        return self.dev.send_recv((CCProtocolPacker.version()), timeout=1000).split('\n')

    def sign_message_start(self, path, msg):
        self.dev.send_recv((CCProtocolPacker.sign_message(msg, path)), timeout=None)

    def sign_message_poll(self):
        return self.dev.send_recv((CCProtocolPacker.get_signed_msg()), timeout=None)

    def sign_transaction_start(self, raw_psbt, finalize=True):
        assert 20 <= len(raw_psbt) < MAX_TXN_LEN, 'PSBT is too big'
        dlen, chk = self.dev.upload_file(raw_psbt)
        resp = self.dev.send_recv(CCProtocolPacker.sign_transaction(dlen, chk, finalize=finalize), timeout=None)
        if resp != None:
            raise ValueError(resp)

    def sign_transaction_poll(self):
        return self.dev.send_recv((CCProtocolPacker.get_signed_txn()), timeout=None)

    def download_file(self, length, checksum, file_number=1):
        return self.dev.download_file(length, checksum, file_number=file_number)


class Coldcard_KeyStore(Hardware_KeyStore):
    hw_type = 'coldcard'
    device = 'Coldcard'

    def __init__(self, d):
        Hardware_KeyStore.__init__(self, d)
        self.force_watching_only = False
        self.ux_busy = False
        lab = d['label']
        if hasattr(lab, 'xfp'):
            self.ckcc_xfp = lab.xfp
            self.ckcc_xpub = lab.xpub
        else:
            self.ckcc_xfp = d['ckcc_xfp']
            self.ckcc_xpub = d['ckcc_xpub']

    def dump(self):
        d = Hardware_KeyStore.dump(self)
        d['ckcc_xfp'] = self.ckcc_xfp
        d['ckcc_xpub'] = self.ckcc_xpub
        return d

    def get_derivation(self):
        return self.derivation

    def get_client(self):
        rv = self.plugin.get_client(self)
        if rv:
            rv.verify_connection(self.ckcc_xfp, self.ckcc_xpub)
        return rv

    def give_error(self, message, clear_client=False):
        self.logger.info(message)
        if not self.ux_busy:
            self.handler.show_error(message)
        else:
            self.ux_busy = False
        if clear_client:
            self.client = None
        raise UserFacingException(message)

    def wrap_busy(func):

        def wrapper(self, *args, **kwargs):
            try:
                self.ux_busy = True
                return func(self, *args, **kwargs)
            finally:
                self.ux_busy = False

        return wrapper

    def decrypt_message(self, pubkey, message, password):
        raise UserFacingException(_('Encryption and decryption are currently not supported for {}').format(self.device))

    @wrap_busy
    def sign_message(self, sequence, message, password):
        try:
            msg = message.encode('ascii', errors='strict')
            assert 1 <= len(msg) <= MSG_SIGNING_MAX_LENGTH
        except (UnicodeError, AssertionError):
            self.handler.show_error('Only short (%d max) ASCII messages can be signed.' % MSG_SIGNING_MAX_LENGTH)
            return b''
        else:
            client = self.get_client()
            path = self.get_derivation() + '/%d/%d' % sequence
            try:
                cl = self.get_client()
                try:
                    self.handler.show_message('Signing message (using %s)...' % path)
                    cl.sign_message_start(path, msg)
                    while 1:
                        time.sleep(0.25)
                        resp = cl.sign_message_poll()
                        if resp is not None:
                            break

                finally:
                    self.handler.finished()

                assert len(resp) == 2
                addr, raw_sig = resp
                assert 40 < len(raw_sig) <= 65
                return raw_sig
            except (CCUserRefused, CCBusyError) as exc:
                try:
                    self.handler.show_error(str(exc))
                finally:
                    exc = None
                    del exc

            except CCProtoError as exc:
                try:
                    self.logger.exception('Error showing address')
                    self.handler.show_error('{}\n\n{}'.format(_('Error showing address') + ':', str(exc)))
                finally:
                    exc = None
                    del exc

            except Exception as e:
                try:
                    self.give_error(e, True)
                finally:
                    e = None
                    del e

            return b''

    def build_psbt(self, tx: Transaction, wallet=None, xfp=None):
        if xfp is None:
            xfp = self.ckcc_xfp
        inputs = tx.inputs()
        if 'prev_tx' not in inputs[0]:
            assert wallet, 'need wallet reference'
            wallet.add_hw_info(tx)
        assert tx.output_info is not None, 'need data about outputs'
        base_path = pack('<I', xfp)
        for x in self.get_derivation()[2:].split('/'):
            if x.endswith("'"):
                x = int(x[:-1]) | 2147483648
            else:
                x = int(x)
            base_path += pack('<I', x)

        subkeys = {}
        derivations = self.get_tx_derivations(tx)
        for xpubkey in derivations:
            pubkey = xpubkey_to_pubkey(xpubkey)
            aa, bb = derivations[xpubkey]
            assert 0 <= aa < 2147483648
            assert 0 <= bb < 2147483648
            subkeys[bfh(pubkey)] = base_path + pack('<II', aa, bb)

        for txin in inputs:
            if txin['type'] == 'coinbase':
                self.give_error('Coinbase not supported')
            if txin['type'] in ('p2sh', 'p2wsh-p2sh', 'p2wsh'):
                self.give_error('No support yet for inputs of type: ' + txin['type'])

        out_fd = io.BytesIO()
        out_fd.write(b'psbt\xff')

        def write_kv(ktype, val, key=b''):
            out_fd.write(my_var_int(1 + len(key)))
            out_fd.write(bytes([ktype]) + key)
            if isinstance(val, str):
                val = bfh(val)
            out_fd.write(my_var_int(len(val)))
            out_fd.write(val)

        class CustomTXSerialization(Transaction):

            @classmethod
            def input_script(cls, txin, estimate_size=False):
                return ''

        unsigned = bfh(CustomTXSerialization(tx.serialize()).serialize_to_network(witness=False))
        write_kv(PSBT_GLOBAL_UNSIGNED_TX, unsigned)
        out_fd.write(b'\x00')
        for txin in inputs:
            if Transaction.is_segwit_input(txin):
                utxo = txin['prev_tx'].outputs()[txin['prevout_n']]
                spendable = txin['prev_tx'].serialize_output(utxo)
                write_kv(PSBT_IN_WITNESS_UTXO, spendable)
            else:
                write_kv(PSBT_IN_NON_WITNESS_UTXO, str(txin['prev_tx']))
            pubkeys, x_pubkeys = tx.get_sorted_pubkeys(txin)
            pubkeys = [bfh(k) for k in pubkeys]
            for k in pubkeys:
                write_kv(PSBT_IN_BIP32_DERIVATION, subkeys[k], k)
                if txin['type'] == 'p2wpkh-p2sh':
                    assert len(pubkeys) == 1, 'can be only one redeem script per input'
                    pa = hash_160(k)
                    assert len(pa) == 20
                    write_kv(PSBT_IN_REDEEM_SCRIPT, b'\x00\x14' + pa)

            out_fd.write(b'\x00')

        for o in tx.outputs():
            if o.address in tx.output_info:
                output_info = tx.output_info.get(o.address)
                index, xpubs = output_info.address_index, output_info.sorted_xpubs
                if index[0] == 1 and len(index) == 2:
                    if not len(xpubs) == 1:
                        raise AssertionError
                    else:
                        xpubkey = xpubs[0]
                        aa, bb = index
                        assert 0 <= aa < 2147483648
                        assert 0 <= bb < 2147483648
                    deriv = base_path + pack('<II', aa, bb)
                    pubkey = bfh(self.get_pubkey_from_xpub(xpubkey, index))
                    write_kv(PSBT_OUT_BIP32_DERIVATION, deriv, pubkey)
                    if output_info.script_type == 'p2wpkh-p2sh':
                        pa = hash_160(pubkey)
                        assert len(pa) == 20
                        write_kv(PSBT_OUT_REDEEM_SCRIPT, b'\x00\x14' + pa)
            out_fd.write(b'\x00')

        return out_fd.getvalue()

    @wrap_busy
    def sign_transaction(self, tx, password):
        if tx.is_complete():
            return
            client = self.get_client()
            if not client.dev.master_fingerprint == self.ckcc_xfp:
                raise AssertionError
        else:
            raw_psbt = self.build_psbt(tx)
            try:
                try:
                    self.handler.show_message('Authorize Transaction...')
                    client.sign_transaction_start(raw_psbt, True)
                    while 1:
                        time.sleep(0.25)
                        resp = client.sign_transaction_poll()
                        if resp is not None:
                            break

                    rlen, rsha = resp
                    new_raw = client.download_file(rlen, rsha)
                finally:
                    self.handler.finished()

            except (CCUserRefused, CCBusyError) as exc:
                try:
                    self.logger.info(f"Did not sign: {exc}")
                    self.handler.show_error(str(exc))
                    return
                finally:
                    exc = None
                    del exc

            except BaseException as e:
                try:
                    self.logger.exception('')
                    self.give_error(e, True)
                    return
                finally:
                    e = None
                    del e

        tx.update(bh2u(new_raw))

    @staticmethod
    def _encode_txin_type(txin_type):
        return {'standard':AF_CLASSIC, 
         'p2pkh':AF_CLASSIC,  'p2sh':AF_P2SH, 
         'p2wpkh-p2sh':AF_P2WPKH_P2SH, 
         'p2wpkh':AF_P2WPKH, 
         'p2wsh-p2sh':AF_P2WSH_P2SH, 
         'p2wsh':AF_P2WSH}[txin_type]

    @wrap_busy
    def show_address(self, sequence, txin_type):
        client = self.get_client()
        address_path = self.get_derivation()[2:] + '/%d/%d' % sequence
        addr_fmt = self._encode_txin_type(txin_type)
        try:
            try:
                self.handler.show_message(_('Showing address ...'))
                dev_addr = client.show_address(address_path, addr_fmt)
            finally:
                self.handler.finished()

        except CCProtoError as exc:
            try:
                self.logger.exception('Error showing address')
                self.handler.show_error('{}\n\n{}'.format(_('Error showing address') + ':', str(exc)))
            finally:
                exc = None
                del exc

        except BaseException as exc:
            try:
                self.logger.exception('')
                self.handler.show_error(exc)
            finally:
                exc = None
                del exc


class ColdcardPlugin(HW_PluginBase):
    keystore_class = Coldcard_KeyStore
    minimum_library = (0, 7, 2)
    client = None
    DEVICE_IDS = [
     (
      COINKITE_VID, CKCC_PID),
     (
      COINKITE_VID, CKCC_SIMULATED_PID)]
    SUPPORTED_XTYPES = ('standard', 'p2wpkh', 'p2wpkh-p2sh')

    def __init__(self, parent, config, name):
        HW_PluginBase.__init__(self, parent, config, name)
        self.libraries_available = self.check_libraries_available()
        if not self.libraries_available:
            return
        self.device_manager().register_devices(self.DEVICE_IDS)
        self.device_manager().register_enumerate_func(self.detect_simulator)

    def get_library_version(self):
        import ckcc
        try:
            version = ckcc.__version__
        except AttributeError:
            version = 'unknown'

        if requirements_ok:
            return version
        raise LibraryFoundButUnusable(library_version=version)

    def detect_simulator(self):
        fn = CKCC_SIMULATOR_PATH
        if os.path.exists(fn):
            return [
             Device(path=fn, interface_number=(-1),
               id_=fn,
               product_key=(
              COINKITE_VID, CKCC_SIMULATED_PID),
               usage_page=0,
               transport_ui_string='simulator')]
        return []

    def create_client(self, device, handler):
        if handler:
            self.handler = handler
        try:
            rv = CKCCClient(self, handler, (device.path), is_simulator=(device.product_key[1] == CKCC_SIMULATED_PID))
            return rv
        except:
            self.logger.info('late failure connecting to device?')
            return

    def setup_device(self, device_info, wizard, purpose):
        devmgr = self.device_manager()
        device_id = device_info.device.id_
        client = devmgr.client_by_id(device_id)
        if client is None:
            raise UserFacingException(_('Failed to create a client for this device.') + '\n' + _('Make sure it is in the correct state.'))
        client.handler = self.create_handler(wizard)

    def get_xpub(self, device_id, derivation, xtype, wizard):
        if xtype not in self.SUPPORTED_XTYPES:
            raise ScriptTypeNotSupported(_('This type of script is not supported with {}.').format(self.device))
        devmgr = self.device_manager()
        client = devmgr.client_by_id(device_id)
        client.handler = self.create_handler(wizard)
        client.ping_check()
        xpub = client.get_xpub(derivation, xtype)
        return xpub

    def get_client(self, keystore, force_pair=True):
        devmgr = self.device_manager()
        handler = keystore.handler
        with devmgr.hid_lock:
            client = devmgr.client_for_keystore(self, handler, keystore, force_pair)
        if client is not None:
            client.ping_check()
        return client

    def show_address(self, wallet, address, keystore=None):
        if keystore is None:
            keystore = wallet.get_keystore()
        else:
            return self.show_address_helper(wallet, address, keystore) or None
        if type(wallet) is not Standard_Wallet:
            keystore.handler.show_error(_('This function is only available for standard wallets when using {}.').format(self.device))
            return
        sequence = wallet.get_address_index(address)
        txin_type = wallet.get_txin_type(address)
        keystore.show_address(sequence, txin_type)