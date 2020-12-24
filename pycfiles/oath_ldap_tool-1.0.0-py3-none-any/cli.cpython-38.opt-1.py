# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/cli.py
# Compiled at: 2020-03-29 19:33:23
# Size of source mod 2**32: 5437 bytes
"""
OATH-LDAP command-line tool
"""
import sys, os, argparse
from .decpin import decpin as cli_decpin
from .genkey import genkey as cli_genkey
from .ykadd import ykadd as cli_ykadd
from .ykinfo import ykinfo as cli_ykinfo
from .ykinit import ykinit as cli_ykinit
__all__ = [
 'main',
 'cli_args']

def cli_args():
    """
    CLI arguments
    """
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(prog=script_name,
      formatter_class=(argparse.ArgumentDefaultsHelpFormatter),
      description='OATH-LDAP tool')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_decpin = subparsers.add_parser('decpin',
      help='sub-command decpin',
      description=(cli_decpin.__doc__))
    parser_decpin.add_argument('-H',
      '--ldap-url', dest='ldap_url',
      help='OATH-LDAP server URL',
      required=True)
    parser_decpin.add_argument('-D',
      '--admin-dn', dest='admin_dn',
      help='bind-DN to use for admin login',
      required=True)
    parser_decpin.add_argument('-p',
      '--key-path', dest='key_path',
      help='path where key files are stored',
      required=True)
    parser_decpin.add_argument('-i',
      '--token-id', dest='token_id',
      help='token identifier in OATH-LDAP entry',
      type=str,
      required=True)
    parser_decpin.set_defaults(func=cli_decpin)
    parser_genkey = subparsers.add_parser('genkey',
      help='sub-command genkey',
      description=(cli_genkey.__doc__))
    parser_genkey.add_argument('-p',
      '--key-path', dest='key_path',
      help='path where to store generated key pair files',
      required=True)
    parser_genkey.add_argument('-s',
      '--key-size', dest='key_size',
      default=2048,
      help='key size of RSA key pair',
      type=int,
      required=False)
    parser_genkey.set_defaults(func=cli_genkey)
    parser_ykinfo = subparsers.add_parser('ykinfo',
      help='sub-command ykinfo',
      description=(cli_ykinfo.__doc__))
    parser_ykinfo.set_defaults(func=cli_ykinfo)
    parser_ykadd = subparsers.add_parser('ykadd',
      help='sub-command ykadd',
      description=(cli_ykadd.__doc__))
    parser_ykadd.add_argument('-H',
      '--ldap-url', dest='ldap_url',
      help='OATH-LDAP server URL incl. search parameters',
      required=True)
    parser_ykadd.add_argument('-D',
      '--admin-dn', dest='admin_dn',
      help='bind-DN to use for admin login',
      required=True)
    parser_ykadd.add_argument('-o',
      '--owner', dest='person_id',
      help='unique name or identifier to search for owner entry',
      required=True)
    parser_ykadd.add_argument('-l',
      '--ldif-template', dest='ldif_template',
      default='',
      help='base DN to be used for token entry',
      required=True)
    parser_ykadd.add_argument('-s',
      '--serial', dest='serial_nr',
      help='serial number of new Yubikey token',
      type=int,
      required=False)
    parser_ykadd.set_defaults(func=cli_ykadd)
    parser_ykinit = subparsers.add_parser('ykinit',
      help='sub-command ykinit',
      description=(cli_ykinit.__doc__))
    parser_ykinit.add_argument('-H',
      '--ldap-url', dest='ldap_url',
      help='OATH-LDAP server URL',
      required=True)
    parser_ykinit.add_argument('-k',
      '--public-key', dest='pubkey',
      help='Public key file to encrypt Yubikey shared secrets',
      required=False)
    parser_ykinit.add_argument('-p',
      '--new-slot-password', dest='access_code',
      default='',
      help='New Yubikey device password')
    parser_ykinit.add_argument('-o',
      '--old-slot-password', dest='current_access_code',
      help='Currently valid Yubikey device password')
    parser_ykinit.add_argument('-c',
      '--continue', dest='continous',
      default=False,
      action='store_true',
      help='Continous operation mode')
    parser_ykinit.set_defaults(func=cli_ykinit)
    return parser.parse_args()


def main():
    """
    the main entry point
    """
    args = cli_args()
    try:
        args.func
    except AttributeError:
        pass
    else:
        args.func(args.func.__name__, args)


if __name__ == '__main__':
    main()