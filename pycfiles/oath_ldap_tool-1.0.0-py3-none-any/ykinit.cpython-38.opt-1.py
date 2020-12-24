# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/ykinit.py
# Compiled at: 2020-03-29 20:41:46
# Size of source mod 2**32: 11748 bytes
"""
oathldap_tool.ykinit -- sub-command for initializing a Yubikey token
"""
import time, sys, os, json
from usb.core import USBError
from jwcrypto.jwk import JWK
from jwcrypto.jwe import JWE
import ldap0
from ldap0 import LDAPError
from ldap0.ldapurl import LDAPUrl
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.pw import random_string
from .__about__ import __version__
from .yubikey import YK_PASSWORD_ALPHABET, YubiKeySearchError, YKTokenDevice
from . import SEP_LINE, ErrorExit, cli_output
JWE_DEFAULT_ALG = 'RSA-OAEP'
JWE_DEFAULT_ENC = 'A256GCM'
ABORT_MSG = 'Aborted -> please insert new Yubikey'
OATH_TOKEN_BINDDN_TMPL = 'serialNumber=yubikey-{unique_id},{search_base}'

class OathLDAPConn(ReconnectLDAPObject):
    __doc__ = '\n    OATH-LDAP connection\n    '

    def __init__(self, ldap_uri, who, cred, **kwargs):
        (ReconnectLDAPObject.__init__)(self, ldap_uri, **kwargs)
        self.set_option(ldap0.OPT_NETWORK_TIMEOUT, 15.0)
        self.simple_bind_s(who, cred)
        self.bound_dn = self.whoami_s()[3:]

    def get_hotp_params(self, token_dn=None):
        """
        read some HOTP parameters from token and policy entries
        """
        token = self.read_s((token_dn or self.bound_dn),
          filterstr='(objectClass=oathHOTPToken)',
          attrlist=[
         'oathHOTPParams',
         'oathTokenIdentifier'])
        token_params = self.read_s((token.entry_s['oathHOTPParams'][0]),
          filterstr='(objectClass=oathHOTPParams)',
          attrlist=[
         'oathEncKey',
         'oathHMACAlgorithm',
         'oathOTPLength'])
        if 'oathEncKey' in token_params.entry_s:
            enc_key = JWK(**json.loads(token_params.entry_s['oathEncKey'][0]))
        else:
            enc_key = None
        return (token.entry_s.get('oathTokenIdentifier', [''])[0],
         token_params.entry_s['oathHMACAlgorithm'][0],
         int(token_params.entry_s['oathOTPLength'][0]),
         enc_key)

    def update_token(self, otp_secret, token_pin, token_dn=None):
        """
        Write OATH-LDAP attributes, especially the already encrypted
        :otp_secret:, to the OATH-LDAP token entry this connection is bound as.
        """
        self.modify_s(token_dn or self.bound_dn, [
         (
          ldap0.MOD_ADD, b'oathHOTPCounter', [b'0']),
         (
          ldap0.MOD_REPLACE, b'oathTokenPIN', [token_pin.encode('utf-8')]),
         (
          ldap0.MOD_ADD, b'oathSecret', [otp_secret.encode('utf-8')])])


def jwk_read(key_filename):
    """
    reads a JWK public key from file and returns the JWK object
    """
    with open(key_filename, 'rb') as (pubkey_file):
        pk_json = pubkey_file.read()
    return JWK(**json.loads(pk_json))


def jwe_encrypt(jwk_obj, plaintext, alg=JWE_DEFAULT_ALG, enc=JWE_DEFAULT_ENC):
    """
    returns JWE strings with :plaintext: being asymmetrically encrypted
    with public key read from file with filename :key_filename:
    """
    jwe_obj = JWE(plaintext=plaintext)
    jwe_obj.add_recipient(jwk_obj,
      header=(json.dumps(dict(alg=alg,
      enc=enc,
      kid=(jwk_obj.key_id)))))
    return jwe_obj.serialize()


def ask_access_code():
    """
    interactively ask for current slot password repeately in case of input error
    """
    current_access_code = input('Provide old slot password --> ')
    while current_access_code:
        current_access_code = len(current_access_code) == 6 and current_access_code.isalnum() or input('Wrong format of slot password => try again')

    return current_access_code


def interactive_ldapconnect--- This code section failed: ---

 L. 158         0  LOAD_GLOBAL              LDAPUrl
                2  LOAD_FAST                'ldap_url'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'ldap_url_obj'

 L. 159         8  LOAD_GLOBAL              OATH_TOKEN_BINDDN_TMPL
               10  LOAD_ATTR                format

 L. 160        12  LOAD_FAST                'serial'

 L. 161        14  LOAD_FAST                'ldap_url_obj'
               16  LOAD_ATTR                dn

 L. 159        18  LOAD_CONST               ('unique_id', 'search_base')
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  STORE_FAST               'ldap_who'

 L. 164        24  LOAD_GLOBAL              cli_output

 L. 166        26  LOAD_STR                 'Enter both enrollment password parts for Yubikey no. %s or remove YubiKey device and hit [ENTER] to rescan\nLDAP-DN: %r'

 L. 169        28  LOAD_FAST                'serial'
               30  LOAD_FAST                'ldap_who'
               32  BUILD_TUPLE_2         2 

 L. 165        34  BINARY_MODULO    

 L. 164        36  CALL_FUNCTION_1       1  ''
               38  POP_TOP          

 L. 171        40  LOAD_GLOBAL              input
               42  LOAD_STR                 'Part #1 --> '
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'ldap_initpw1'

 L. 172        48  LOAD_FAST                'ldap_initpw1'
               50  POP_JUMP_IF_TRUE     60  'to 60'

 L. 173        52  LOAD_GLOBAL              ErrorExit
               54  LOAD_GLOBAL              ABORT_MSG
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 174        60  LOAD_GLOBAL              input
               62  LOAD_STR                 'Part #2 --> '
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'ldap_initpw2'

 L. 175        68  LOAD_FAST                'ldap_initpw2'
               70  POP_JUMP_IF_TRUE     80  'to 80'

 L. 176        72  LOAD_GLOBAL              ErrorExit
               74  LOAD_GLOBAL              ABORT_MSG
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 177        80  SETUP_FINALLY       106  'to 106'

 L. 178        82  LOAD_GLOBAL              OathLDAPConn

 L. 179        84  LOAD_FAST                'ldap_url_obj'
               86  LOAD_METHOD              connect_uri
               88  CALL_METHOD_0         0  ''

 L. 180        90  LOAD_FAST                'ldap_who'

 L. 181        92  LOAD_FAST                'ldap_initpw1'
               94  LOAD_FAST                'ldap_initpw2'
               96  BINARY_ADD       

 L. 178        98  CALL_FUNCTION_3       3  ''
              100  STORE_FAST               'oath_ldap'
              102  POP_BLOCK        
              104  BREAK_LOOP          140  'to 140'
            106_0  COME_FROM_FINALLY    80  '80'

 L. 183       106  DUP_TOP          
              108  LOAD_GLOBAL              ldap0
              110  LOAD_ATTR                INVALID_CREDENTIALS
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   134  'to 134'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 184       122  LOAD_GLOBAL              cli_output
              124  LOAD_STR                 'Enrollment password(s) wrong => try again'
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          
              130  POP_EXCEPT       
              132  JUMP_BACK            24  'to 24'
            134_0  COME_FROM           114  '114'
              134  END_FINALLY      

 L. 186       136  BREAK_LOOP          140  'to 140'
              138  JUMP_BACK            24  'to 24'

 L. 187       140  LOAD_FAST                'oath_ldap'
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 118


def ykinit_once(args, jwk_obj):
    """
    Run as stand-alone script
    """
    try:
        sys.stdout.write('\nWaiting for single Yubikey device.')
        while True:
            try:
                yk_device = YKTokenDevice.search()
            except (YubiKeySearchError, USBError):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.8)
            else:
                sys.stdout.write('\n')
                break

        access_code = args.access_code or random_string(YK_PASSWORD_ALPHABET, 6)
        if not (len(access_code) != 6 or access_code.isalnum()):
            raise ErrorExit('Slot password must be exactly six (6) alpha-numeric ASCII characters!')
        cli_output('Found Yubikey device no. %s' % yk_device.key.serial())
        cli_output(yk_device.info_msg())
        enabled_slots = yk_device.enabled_slots()
        if enabled_slots:
            confirm_input = input('Confirm with word "reset" to clear the device or remove Yubikey device and hit [ENTER] to rescan --> ')
            if confirm_input.lower() != 'reset':
                raise ErrorExit(ABORT_MSG)
            elif args.current_access_code:
                current_access_code = args.current_access_code
            else:
                current_access_code = ask_access_code()
            cli_output('Clearing slot(s) %s...' % enabled_slots)
            for slot in yk_device.enabled_slots():
                yk_device.reset_slot(slot, current_access_code)
            else:
                yk_device.clear(current_access_code)

        yk_serial = yk_device.key.serial()
        del yk_device
        clear_time = time.time()
        oath_ldap = interactive_ldapconnect(args.ldap_url, yk_serial)
        oath_identifier, _, otp_length, oath_enckey = oath_ldap.get_hotp_params()
        if oath_enckey is None:
            oath_enckey = jwk_obj
        if oath_enckey is None:
            raise ErrorExit('No public key available to encrypt shared secret!')
        cli_output('Key used for encrypting secrets:')
        cli_output(('kid: %s\nthumbprint: %s' % (oath_enckey.key_id, oath_enckey.thumbprint())),
          lf_before=0)
        oath_secret = os.urandom(20)
        oath_ldap.update_token(jwe_encrypt(oath_enckey, oath_secret), jwe_encrypt(oath_enckey, access_code))
        cli_output('Updated secret in OATH-LDAP entry %r' % oath_ldap.bound_dn)
        oath_ldap.unbind_s()
        sleep_time = 5.0 - (time.time() - clear_time)
        if sleep_time >= 0.0:
            cli_output('Waiting %0.1f secs until Yubikey reconnect...' % sleep_time)
            time.sleep(sleep_time)
        yk_device = YKTokenDevice.search()
        if yk_serial != yk_device.key.serial():
            raise ErrorExit('Device serial no. changed!')
        cli_output('Initialize Yubikey device no. %s' % yk_device.key.serial())
        cli_output(('*** Write down new password for Yubikey %s and keep in safe place -> %s ***' % (
         yk_device.key.serial(),
         access_code)),
          lf_before=2,
          lf_after=2)
        yk_device.initialize(oath_secret, otp_length, oath_identifier, access_code)
    except USBError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except LDAPError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except ErrorExit as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except YubiKeySearchError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    else:
        cli_output('Yubikey successfully initialized. Unplug it right now!', lf_after=2)
        if args.continous:
            input('Hit a key to initialize another Yubikey token...')
        cli_output(SEP_LINE)


def ykinit(command_name, args):
    """
    Initializes a Yubikey token for HOTP and sends encrypted shared secret
    to OATH-LDAP server after authenticating as the token entry with the
    enrollment password
    """
    cli_output(SEP_LINE, lf_before=0, lf_after=0)
    cli_output('OATH-LDAP {0} v{1}'.format(command_name, __version__))
    cli_output(SEP_LINE, lf_before=0)
    if args.pubkey:
        cli_output('Read JWK public key file %s' % args.pubkey)
        try:
            jwk_obj = jwk_read(args.pubkey)
        except IOError as err:
            try:
                cli_output('Error reading JWK public key file %s -> %r' % (args.pubkey, err))
                sys.exit(1)
            finally:
                err = None
                del err

        else:
            cli_output(('kid: %s\nthumbprint: %s' % (jwk_obj.key_id, jwk_obj.thumbprint())), lf_before=0)
    else:
        cli_output('No JWK public key specified')
        jwk_obj = None
        while True:
            ykinit_once(args, jwk_obj)
            if not args.continous:
                break