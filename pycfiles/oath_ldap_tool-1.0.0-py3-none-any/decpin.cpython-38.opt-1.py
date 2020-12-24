# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/decpin.py
# Compiled at: 2020-03-29 18:51:16
# Size of source mod 2**32: 3800 bytes
"""
oathldap_tool.decpin -- sub-command for extracting decrypted PIN from token entry
"""
import os, time, sys, getpass, json, glob
try:
    from jwcrypto.jwk import JWK
    from jwcrypto.jwe import JWE
except ImportError:
    JWE = JWK = None
else:
    import ldap0, ldap0.filter
    from ldap0 import LDAPError
    from ldap0.ldapurl import LDAPUrl
    from .__about__ import __version__
    from . import ABORT_MSG, SEP_LINE, ErrorExit, cli_output
    from . import interactive_ldapconnect
    TOKEN_FILTER_TMPL = '(&(objectClass=oathToken)(oathTokenPIN=*)(|(serialNumber={0})(oathTokenIdentifier={0})(oathTokenSerialNumber={0})))'

    def _load_key(key_path, key_id):
        """
    Load JWE keys defined by globbing pattern in :key_files:
    """
        for private_key_filename in glob.glob(os.path.join(key_path, '*.priv')):
            with open(private_key_filename, 'rb') as (key_file):
                privkey_json = key_file.read()
            private_key = JWK(**json.loads(privkey_json))
            if key_id == private_key.key_id:
                break
            raise ErrorExit('No private key with key id %r' % (key_id,))
            return private_key


    def _decrypt_pin(key_path, oath_pin):
        """
    This methods extracts and decrypts the token's OATH shared
    secret from the token's LDAP entry given in argument
    :token_entry:
    """
        if not JWE:
            raise ErrorExit('Package jwcrypto not installed')
        json_s = json.loads(oath_pin)
        key_id = json_s['header']['kid']
        jwe_decrypter = JWE()
        oath_master_secret = _load_key(key_path, key_id)
        jwe_decrypter.deserialize(oath_pin, oath_master_secret)
        return jwe_decrypter.plaintext


    def decpin(command_name, args):
        """
    Retrieves and decrypts PIN from token entry in OATH-LDAP server
    """
        cli_output(SEP_LINE, lf_before=0, lf_after=0)
        cli_output('OATH-LDAP {0} v{1}'.format(command_name, __version__))
        cli_output(SEP_LINE, lf_before=0)
        try:
            ldap_url = LDAPUrl(args.ldap_url)
            oath_ldap = interactive_ldapconnect(ldap_url.connect_uri(), args.admin_dn)
            token_filter = TOKEN_FILTER_TMPL.format(ldap0.filter.escape_str(args.token_id))
            token = oath_ldap.find_unique_entry((ldap_url.dn),
              (ldap_url.scope or ldap0.SCOPE_SUBTREE),
              token_filter,
              attrlist=[
             'oathTokenPIN'])
            oath_ldap.unbind_s()
            cli_output(SEP_LINE, lf_before=0, lf_after=0)
            cli_output('Found token entry %r' % token.dn_s)
            cli_output('Decrypted PIN: {0}'.format(_decrypt_pin(args.key_path, token.entry_as['oathTokenPIN'][0]).decode('utf-8')))
            cli_output(SEP_LINE, lf_before=0, lf_after=1)
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