# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/genkey.py
# Compiled at: 2020-03-29 16:31:02
# Size of source mod 2**32: 1956 bytes
"""
oathldap_tool.ykadd -- sub-command for generating OATH-LDAP master key pair
"""
import time, os
from jwcrypto.jwk import JWK
from .__about__ import __version__
from . import cli_output
KEY_TYPE = 'RSA'
KEYID_FORMAT = 'oathldap_master_key_{0}'
KEY_PRIV_PERMS = 384
KEY_PUB_PERMS = 420

def genkey(command_name, args):
    """
    generate new RSA key pair for encrypted shared secrets
    """
    key_id = KEYID_FORMAT.format(time.strftime('%Y%m%d%H%M', time.gmtime(time.time())))
    privkey_filename = os.path.join(args.key_path, key_id + '.priv')
    pubkey_filename = os.path.join(args.key_path, key_id + '.pub')
    cli_output(('Generating RSA-{0:d} key pair...'.format(args.key_size)), lf_before=0)
    key = JWK(kty=KEY_TYPE,
      use='enc',
      generate=KEY_TYPE,
      kid=key_id,
      size=(args.key_size))
    with open(privkey_filename, 'w', encoding='utf-8') as (fileobj):
        fileobj.write(key.export())
    os.chmod(privkey_filename, KEY_PRIV_PERMS)
    cli_output('wrote {0}'.format(privkey_filename, lf_before=0))
    with open(pubkey_filename, 'w', encoding='utf-8') as (fileobj):
        fileobj.write(key.export_public())
    os.chmod(pubkey_filename, KEY_PUB_PERMS)
    cli_output(('wrote {0}'.format(pubkey_filename)), lf_before=0)