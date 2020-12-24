# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/ledger/ledger.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 27890 bytes
from struct import pack, unpack
import hashlib, sys, traceback
from electrum import ecc
from electrum.bitcoin import TYPE_ADDRESS, int_to_hex, var_int, is_segwit_script_type
from electrum.bip32 import BIP32Node
from electrum.i18n import _
from electrum.keystore import Hardware_KeyStore
from electrum.transaction import Transaction
from electrum.wallet import Standard_Wallet
from electrum.util import bfh, bh2u, versiontuple, UserFacingException
from electrum.base_wizard import ScriptTypeNotSupported
from electrum.logging import get_logger
from ..hw_wallet import HW_PluginBase
from hw_wallet.plugin import is_any_tx_output_on_change_branch
_logger = get_logger(__name__)
try:
    import hid
    from btchip.btchipComm import HIDDongleHIDAPI, DongleWait
    import btchip.btchip as btchip
    from btchip.btchipUtils import compress_public_key, format_transaction, get_regular_input_script, get_p2sh_input_script
    import btchip.bitcoinTransaction as bitcoinTransaction
    from btchip.btchipFirmwareWizard import checkFirmware, updateFirmware
    from btchip.btchipException import BTChipException
    BTCHIP = True
    BTCHIP_DEBUG = False
except ImportError:
    BTCHIP = False

MSG_NEEDS_FW_UPDATE_GENERIC = _('Firmware version too old. Please update at') + ' https://www.ledgerwallet.com'
MSG_NEEDS_FW_UPDATE_SEGWIT = _('Firmware version (or "Bitcoin" app) too old for Segwit support. Please update at') + ' https://www.ledgerwallet.com'
MULTI_OUTPUT_SUPPORT = '1.1.4'
SEGWIT_SUPPORT = '1.1.10'
SEGWIT_SUPPORT_SPECIAL = '1.0.4'

def test_pin_unlocked(func):
    """Function decorator to test the Ledger for being unlocked, and if not,
    raise a human-readable exception.
    """

    def catch_exception(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except BTChipException as e:
            try:
                if e.sw == 27010:
                    raise UserFacingException(_('Your Ledger is locked. Please unlock it.'))
                else:
                    raise
            finally:
                e = None
                del e

    return catch_exception


class Ledger_Client:

    def __init__(self, hidDevice):
        self.dongleObject = btchip(hidDevice)
        self.preflightDone = False

    def is_pairable(self):
        return True

    def close(self):
        self.dongleObject.dongle.close()

    def timeout(self, cutoff):
        pass

    def is_initialized(self):
        return True

    def label(self):
        return ''

    def i4b(self, x):
        return pack('>I', x)

    def has_usable_connection_with_device(self):
        try:
            self.dongleObject.getFirmwareVersion()
        except BaseException:
            return False
        else:
            return True

    @test_pin_unlocked
    def get_xpub(self, bip32_path, xtype):
        self.checkDevice()
        if xtype in ('p2wpkh', 'p2wsh'):
            if not self.supports_native_segwit():
                raise UserFacingException(MSG_NEEDS_FW_UPDATE_SEGWIT)
        if xtype in ('p2wpkh-p2sh', 'p2wsh-p2sh'):
            if not self.supports_segwit():
                raise UserFacingException(MSG_NEEDS_FW_UPDATE_SEGWIT)
        splitPath = bip32_path.split('/')
        if splitPath[0] == 'm':
            splitPath = splitPath[1:]
            bip32_path = bip32_path[2:]
        fingerprint = 0
        if len(splitPath) > 1:
            prevPath = '/'.join(splitPath[0:len(splitPath) - 1])
            nodeData = self.dongleObject.getWalletPublicKey(prevPath)
            publicKey = compress_public_key(nodeData['publicKey'])
            h = hashlib.new('ripemd160')
            h.update(hashlib.sha256(publicKey).digest())
            fingerprint = unpack('>I', h.digest()[0:4])[0]
        nodeData = self.dongleObject.getWalletPublicKey(bip32_path)
        publicKey = compress_public_key(nodeData['publicKey'])
        depth = len(splitPath)
        lastChild = splitPath[(len(splitPath) - 1)].split("'")
        childnum = int(lastChild[0]) if len(lastChild) == 1 else 2147483648 | int(lastChild[0])
        return BIP32Node(xtype=xtype, eckey=(ecc.ECPubkey(publicKey)),
          chaincode=(nodeData['chainCode']),
          depth=depth,
          fingerprint=(self.i4b(fingerprint)),
          child_number=(self.i4b(childnum))).to_xpub()

    def has_detached_pin_support(self, client):
        try:
            client.getVerifyPinRemainingAttempts()
            return True
        except BTChipException as e:
            try:
                if e.sw == 27904:
                    return False
                raise e
            finally:
                e = None
                del e

    def is_pin_validated(self, client):
        try:
            client.dongle.exchange(bytearray([224, 38, 0, 0, 1, 171]))
        except BTChipException as e:
            try:
                if e.sw == 27010:
                    return False
                if e.sw == 27264:
                    return True
                raise e
            finally:
                e = None
                del e

    def supports_multi_output(self):
        return self.multiOutputSupported

    def supports_segwit(self):
        return self.segwitSupported

    def supports_native_segwit(self):
        return self.nativeSegwitSupported

    def perform_hw1_preflight(self):
        try:
            firmwareInfo = self.dongleObject.getFirmwareVersion()
            firmware = firmwareInfo['version']
            self.multiOutputSupported = versiontuple(firmware) >= versiontuple(MULTI_OUTPUT_SUPPORT)
            self.nativeSegwitSupported = versiontuple(firmware) >= versiontuple(SEGWIT_SUPPORT)
            self.segwitSupported = self.nativeSegwitSupported or firmwareInfo['specialVersion'] == 32 and versiontuple(firmware) >= versiontuple(SEGWIT_SUPPORT_SPECIAL)
            if not checkFirmware(firmwareInfo):
                self.dongleObject.dongle.close()
                raise UserFacingException(MSG_NEEDS_FW_UPDATE_GENERIC)
            try:
                self.dongleObject.getOperationMode()
            except BTChipException as e:
                try:
                    if e.sw == 27013:
                        self.dongleObject.dongle.close()
                        self.handler.get_setup()
                    else:
                        raise e
                finally:
                    e = None
                    del e

            if self.has_detached_pin_support(self.dongleObject):
                if not self.is_pin_validated(self.dongleObject):
                    if self.handler is not None:
                        remaining_attempts = self.dongleObject.getVerifyPinRemainingAttempts()
                        if remaining_attempts != 1:
                            msg = 'Enter your Ledger PIN - remaining attempts : ' + str(remaining_attempts)
                        else:
                            msg = 'Enter your Ledger PIN - WARNING : LAST ATTEMPT. If the PIN is not correct, the dongle will be wiped.'
                        confirmed, p, pin = self.password_dialog(msg)
                        if not confirmed:
                            raise UserFacingException('Aborted by user - please unplug the dongle and plug it again before retrying')
                        pin = pin.encode()
                        self.dongleObject.verifyPin(pin)
        except BTChipException as e:
            try:
                if e.sw == 28586:
                    raise UserFacingException('Dongle is temporarily locked - please unplug it and replug it again')
                else:
                    if e.sw & 65520 == 25536:
                        raise UserFacingException('Invalid PIN - please unplug the dongle and plug it again before retrying')
                    if e.sw == 28416 and e.message == 'Invalid channel':
                        raise UserFacingException("Invalid channel.\nPlease make sure that 'Browser support' is disabled on your device.")
                raise e
            finally:
                e = None
                del e

    def checkDevice(self):
        if not self.preflightDone:
            try:
                self.perform_hw1_preflight()
            except BTChipException as e:
                try:
                    if e.sw == 27904 or e.sw == 26368:
                        raise UserFacingException(_('Device not in Bitcoin mode')) from e
                    raise e
                finally:
                    e = None
                    del e

            self.preflightDone = True

    def password_dialog(self, msg=None):
        response = self.handler.get_word(msg)
        if response is None:
            return (False, None, None)
        return (
         True, response, response)


class Ledger_KeyStore(Hardware_KeyStore):
    hw_type = 'ledger'
    device = 'Ledger'

    def __init__(self, d):
        Hardware_KeyStore.__init__(self, d)
        self.force_watching_only = False
        self.signing = False
        self.cfg = d.get('cfg', {'mode': 0})

    def dump(self):
        obj = Hardware_KeyStore.dump(self)
        obj['cfg'] = self.cfg
        return obj

    def get_derivation(self):
        return self.derivation

    def get_client(self):
        return self.plugin.get_client(self).dongleObject

    def get_client_electrum(self):
        return self.plugin.get_client(self)

    def give_error(self, message, clear_client=False):
        _logger.info(message)
        if not self.signing:
            self.handler.show_error(message)
        else:
            self.signing = False
        if clear_client:
            self.client = None
        raise UserFacingException(message)

    def set_and_unset_signing(func):
        """Function decorator to set and unset self.signing."""

        def wrapper(self, *args, **kwargs):
            try:
                self.signing = True
                return func(self, *args, **kwargs)
            finally:
                self.signing = False

        return wrapper

    def address_id_stripped(self, address):
        change, index = self.get_address_index(address)
        derivation = self.derivation
        address_path = '%s/%d/%d' % (derivation, change, index)
        return address_path[2:]

    def decrypt_message(self, pubkey, message, password):
        raise UserFacingException(_('Encryption and decryption are currently not supported for {}').format(self.device))

    @test_pin_unlocked
    @set_and_unset_signing
    def sign_message(self, sequence, message, password):
        message = message.encode('utf8')
        message_hash = hashlib.sha256(message).hexdigest().upper()
        client = self.get_client()
        address_path = self.get_derivation()[2:] + '/%d/%d' % sequence
        self.handler.show_message('Signing message ...\r\nMessage hash: ' + message_hash)
        try:
            try:
                info = self.get_client().signMessagePrepare(address_path, message)
                pin = ''
                if info['confirmationNeeded']:
                    pin = self.handler.get_auth(info)
                    if not pin:
                        raise UserWarning(_('Cancelled by user'))
                    pin = str(pin).encode()
                signature = self.get_client().signMessageSign(pin)
            except BTChipException as e:
                try:
                    if e.sw == 27264:
                        self.give_error('Unfortunately, this message cannot be signed by the Ledger wallet. Only alphanumerical messages shorter than 140 characters are supported. Please remove any extra characters (tab, carriage return) and retry.')
                    else:
                        if e.sw == 27013:
                            return b''
                        elif e.sw == 27010:
                            raise
                        else:
                            self.give_error(e, True)
                finally:
                    e = None
                    del e

            except UserWarning:
                self.handler.show_error(_('Cancelled by user'))
                return b''
            except Exception as e:
                try:
                    self.give_error(e, True)
                finally:
                    e = None
                    del e

        finally:
            self.handler.finished()

        rLength = signature[3]
        r = signature[4:4 + rLength]
        sLength = signature[(4 + rLength + 1)]
        s = signature[4 + rLength + 2:]
        if rLength == 33:
            r = r[1:]
        if sLength == 33:
            s = s[1:]
        return bytes([31 + (signature[0] & 1)]) + r + s

    @test_pin_unlocked
    @set_and_unset_signing
    def sign_transaction(self, tx, password):
        if tx.is_complete():
            return
            client = self.get_client()
            inputs = []
            inputsPaths = []
            pubKeys = []
            chipInputs = []
            redeemScripts = []
            signatures = []
            changePath = ''
            output = None
            p2shTransaction = False
            segwitTransaction = False
            pin = ''
            self.get_client()
            derivations = self.get_tx_derivations(tx)
            for txin in tx.inputs():
                if txin['type'] == 'coinbase':
                    self.give_error('Coinbase not supported')
                if txin['type'] in ('p2sh', ):
                    p2shTransaction = True
                if txin['type'] in ('p2wpkh-p2sh', 'p2wsh-p2sh'):
                    if not self.get_client_electrum().supports_segwit():
                        self.give_error(MSG_NEEDS_FW_UPDATE_SEGWIT)
                    segwitTransaction = True
                if txin['type'] in ('p2wpkh', 'p2wsh'):
                    if not self.get_client_electrum().supports_native_segwit():
                        self.give_error(MSG_NEEDS_FW_UPDATE_SEGWIT)
                    segwitTransaction = True
                pubkeys, x_pubkeys = tx.get_sorted_pubkeys(txin)
                for i, x_pubkey in enumerate(x_pubkeys):
                    if x_pubkey in derivations:
                        signingPos = i
                        s = derivations.get(x_pubkey)
                        hwAddress = '%s/%d/%d' % (self.get_derivation()[2:], s[0], s[1])
                        break
                else:
                    self.give_error('No matching x_key for sign_transaction')

                redeemScript = Transaction.get_preimage_script(txin)
                txin_prev_tx = txin.get('prev_tx')
                if txin_prev_tx is None:
                    if not Transaction.is_segwit_input(txin):
                        raise UserFacingException(_('Offline signing with {} is not supported for legacy inputs.').format(self.device))
                txin_prev_tx_raw = txin_prev_tx.raw if txin_prev_tx else None
                inputs.append([txin_prev_tx_raw,
                 txin['prevout_n'],
                 redeemScript,
                 txin['prevout_hash'],
                 signingPos,
                 txin.get('sequence', 4294967294),
                 txin.get('value')])
                inputsPaths.append(hwAddress)
                pubKeys.append(pubkeys)

            if p2shTransaction:
                for txin in tx.inputs():
                    if txin['type'] != 'p2sh':
                        self.give_error('P2SH / regular input mixed in same transaction not supported')

            txOutput = var_int(len(tx.outputs()))
            for o in tx.outputs():
                output_type, addr, amount, name_op = (
                 o.type, o.address, o.value, o.name_op)
                txOutput += int_to_hex(amount, 8)
                script = tx.pay_script(output_type, addr, name_op)
                txOutput += var_int(len(script) // 2)
                txOutput += script

            txOutput = bfh(txOutput)
            if not p2shTransaction:
                if not self.get_client_electrum().supports_multi_output():
                    if len(tx.outputs()) > 2:
                        self.give_error('Transaction with more than 2 outputs not supported')
        else:
            has_change = False
            any_output_on_change_branch = is_any_tx_output_on_change_branch(tx)
            for o in tx.outputs():
                assert o.type == TYPE_ADDRESS
                info = tx.output_info.get(o.address)
                if info is not None and len(tx.outputs()) > 1:
                    index = has_change or info.address_index
                    on_change_branch = index[0] == 1
                    if on_change_branch == any_output_on_change_branch:
                        changePath = self.get_derivation()[2:] + '/%d/%d' % index
                        has_change = True
                    else:
                        output = o.address
                else:
                    output = o.address

        self.handler.show_message(_('Confirm Transaction on your Ledger device...'))
        try:
            try:
                for utxo in inputs:
                    sequence = int_to_hex(utxo[5], 4)
                    if segwitTransaction:
                        tmp = bfh(utxo[3])[::-1]
                        tmp += bfh(int_to_hex(utxo[1], 4))
                        tmp += bfh(int_to_hex(utxo[6], 8))
                        chipInputs.append({'value':tmp,  'witness':True,  'sequence':sequence})
                        redeemScripts.append(bfh(utxo[2]))
                    elif not p2shTransaction:
                        txtmp = bitcoinTransaction(bfh(utxo[0]))
                        trustedInput = self.get_client().getTrustedInput(txtmp, utxo[1])
                        trustedInput['sequence'] = sequence
                        chipInputs.append(trustedInput)
                        redeemScripts.append(txtmp.outputs[utxo[1]].script)
                    else:
                        tmp = bfh(utxo[3])[::-1]
                        tmp += bfh(int_to_hex(utxo[1], 4))
                        chipInputs.append({'value':tmp,  'sequence':sequence})
                        redeemScripts.append(bfh(utxo[2]))

                firstTransaction = True
                inputIndex = 0
                rawTx = tx.serialize_to_network()
                self.get_client().enableAlternate2fa(False)
                if segwitTransaction:
                    self.get_client().startUntrustedTransaction(True, inputIndex, chipInputs,
                      (redeemScripts[inputIndex]), version=(tx.version))
                    outputData = self.get_client().finalizeInput(b'', 0, 0, changePath, bfh(rawTx))
                    outputData['outputData'] = txOutput
                    if outputData['confirmationNeeded']:
                        outputData['address'] = output
                        self.handler.finished()
                        pin = self.handler.get_auth(outputData)
                        if not pin:
                            raise UserWarning()
                        self.handler.show_message(_('Confirmed. Signing Transaction...'))
                    while inputIndex < len(inputs):
                        singleInput = [
                         chipInputs[inputIndex]]
                        self.get_client().startUntrustedTransaction(False, 0, singleInput,
                          (redeemScripts[inputIndex]), version=(tx.version))
                        inputSignature = self.get_client().untrustedHashSign((inputsPaths[inputIndex]), pin, lockTime=(tx.locktime))
                        inputSignature[0] = 48
                        signatures.append(inputSignature)
                        inputIndex = inputIndex + 1

                else:
                    while inputIndex < len(inputs):
                        self.get_client().startUntrustedTransaction(firstTransaction, inputIndex, chipInputs,
                          (redeemScripts[inputIndex]), version=(tx.version))
                        outputData = self.get_client().finalizeInput(b'', 0, 0, changePath, bfh(rawTx))
                        outputData['outputData'] = txOutput
                        if outputData['confirmationNeeded']:
                            outputData['address'] = output
                            self.handler.finished()
                            pin = self.handler.get_auth(outputData)
                            if not pin:
                                raise UserWarning()
                            self.handler.show_message(_('Confirmed. Signing Transaction...'))
                        else:
                            inputSignature = self.get_client().untrustedHashSign((inputsPaths[inputIndex]), pin, lockTime=(tx.locktime))
                            inputSignature[0] = 48
                            signatures.append(inputSignature)
                            inputIndex = inputIndex + 1
                        firstTransaction = False

            except UserWarning:
                self.handler.show_error(_('Cancelled by user'))
                return
            except BTChipException as e:
                try:
                    if e.sw in (27013, 27904):
                        return
                    if e.sw == 27010:
                        raise
                    else:
                        self.logger.exception('')
                        self.give_error(e, True)
                finally:
                    e = None
                    del e

            except BaseException as e:
                try:
                    self.logger.exception('')
                    self.give_error(e, True)
                finally:
                    e = None
                    del e

        finally:
            self.handler.finished()

        for i, txin in enumerate(tx.inputs()):
            signingPos = inputs[i][4]
            tx.add_signature_to_txin(i, signingPos, bh2u(signatures[i]))

        tx.raw = tx.serialize()

    @test_pin_unlocked
    @set_and_unset_signing
    def show_address(self, sequence, txin_type):
        client = self.get_client()
        address_path = self.get_derivation()[2:] + '/%d/%d' % sequence
        self.handler.show_message(_('Showing address ...'))
        segwit = is_segwit_script_type(txin_type)
        segwitNative = txin_type == 'p2wpkh'
        try:
            try:
                client.getWalletPublicKey(address_path, showOnScreen=True, segwit=segwit, segwitNative=segwitNative)
            except BTChipException as e:
                try:
                    if e.sw == 27013:
                        pass
                    elif e.sw == 27010:
                        raise
                    else:
                        if e.sw == 27392:
                            self.handler.show_error('{}\n{}\n{}'.format(_('Error showing address') + ':', e, _('Your device might not have support for this functionality.')))
                        else:
                            self.logger.exception('')
                            self.handler.show_error(e)
                finally:
                    e = None
                    del e

            except BaseException as e:
                try:
                    self.logger.exception('')
                    self.handler.show_error(e)
                finally:
                    e = None
                    del e

        finally:
            self.handler.finished()


class LedgerPlugin(HW_PluginBase):
    libraries_available = BTCHIP
    keystore_class = Ledger_KeyStore
    client = None
    DEVICE_IDS = [
     (9601, 6151),
     (9601, 11132),
     (9601, 15228),
     (9601, 19324),
     (11415, 0),
     (11415, 1),
     (11415, 4),
     (11415, 5),
     (11415, 6),
     (11415, 7),
     (11415, 8),
     (11415, 9),
     (11415, 10)]
    SUPPORTED_XTYPES = ('standard', 'p2wpkh-p2sh', 'p2wpkh', 'p2wsh-p2sh', 'p2wsh')

    def __init__(self, parent, config, name):
        self.segwit = config.get('segwit')
        HW_PluginBase.__init__(self, parent, config, name)
        if self.libraries_available:
            self.device_manager().register_devices(self.DEVICE_IDS)

    def get_btchip_device(self, device):
        ledger = False
        if device.product_key[0] == 9601:
            if device.product_key[1] == 15228:
                ledger = True
        if device.product_key[0] == 9601:
            if device.product_key[1] == 19324:
                ledger = True
        if not device.product_key[0] == 11415 or device.interface_number == 0 or device.usage_page == 65440:
            ledger = True
        else:
            return
        dev = hid.device()
        dev.open_path(device.path)
        dev.set_nonblocking(True)
        return HIDDongleHIDAPI(dev, ledger, BTCHIP_DEBUG)

    def create_client(self, device, handler):
        if handler:
            self.handler = handler
        client = self.get_btchip_device(device)
        if client is not None:
            client = Ledger_Client(client)
        return client

    def setup_device(self, device_info, wizard, purpose):
        devmgr = self.device_manager()
        device_id = device_info.device.id_
        client = devmgr.client_by_id(device_id)
        if client is None:
            raise UserFacingException(_('Failed to create a client for this device.') + '\n' + _('Make sure it is in the correct state.'))
        client.handler = self.create_handler(wizard)
        client.get_xpub("m/44'/0'", 'standard')

    def get_xpub(self, device_id, derivation, xtype, wizard):
        if xtype not in self.SUPPORTED_XTYPES:
            raise ScriptTypeNotSupported(_('This type of script is not supported with {}.').format(self.device))
        devmgr = self.device_manager()
        client = devmgr.client_by_id(device_id)
        client.handler = self.create_handler(wizard)
        client.checkDevice()
        xpub = client.get_xpub(derivation, xtype)
        return xpub

    def get_client(self, keystore, force_pair=True):
        devmgr = self.device_manager()
        handler = keystore.handler
        with devmgr.hid_lock:
            client = devmgr.client_for_keystore(self, handler, keystore, force_pair)
        if client is not None:
            client.checkDevice()
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