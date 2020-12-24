# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/ykadd.py
# Compiled at: 2020-03-29 18:09:38
# Size of source mod 2**32: 4212 bytes
"""
oathldap_tool.ykadd -- sub-command for adding LDAP entry for Yubikey token
"""
import time, sys
from usb.core import USBError
import ldap0, ldap0.base
from ldap0 import LDAPError
from ldap0.ldapurl import LDAPUrl
from ldap0.ldif import LDIFParser
from ldap0.tmpl import TemplateEntry
from .__about__ import __version__
from .yubikey import YubiKeySearchError, YKTokenDevice
from . import SEP_LINE, ErrorExit, cli_output
from . import interactive_ldapconnect
OWNER_FILTER_TMPL = '(&(objectClass=inetOrgPerson)(|(uid={0})(mail={0})(uniqueIdentifier={0})(employeeNumber={0})))'

def ykadd(command_name, args):
    """
    Adds Yubikey token entry to OATH-LDAP server
    """
    cli_output(SEP_LINE, lf_before=0, lf_after=0)
    cli_output('OATH-LDAP {0} v{1}'.format(command_name, __version__))
    cli_output(SEP_LINE, lf_before=0)
    try:
        try:
            with open(args.ldif_template, 'rb') as (ldif_file):
                t_dn, t_entry = LDIFParser(ldif_file).list_entry_records()[0]
        except IOError as err:
            try:
                raise ErrorExit('Unable to read LDIF template: %s' % err)
            finally:
                err = None
                del err

        else:
            ldap_url = LDAPUrl(args.ldap_url)
            oath_ldap = interactive_ldapconnect(ldap_url.connect_uri(), args.admin_dn)
            owner_filter = OWNER_FILTER_TMPL.format(ldap0.filter.escape_str(args.person_id))
            if ldap_url.filterstr is not None:
                owner_filter = '(&{0}{1})'.format(ldap_url.filterstr, owner_filter)
            else:
                owner = oath_ldap.find_unique_entry((ldap_url.dn),
                  (ldap_url.scope or ldap0.SCOPE_SUBTREE),
                  owner_filter,
                  attrlist=[
                 '1.1'])
                if args.serial_nr:
                    yk_serial = int(args.serial_nr)
                else:
                    input('Remove Yubikey used for login, press [ENTER] to continue...')
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

                yk_serial = yk_device.key.serial()
                cli_output('Found Yubikey device no. %s' % yk_serial)
                cli_output(yk_device.info_msg())
            token_dn, token_entry = TemplateEntry(t_dn.decode('utf-8'), ldap0.base.decode_entry_dict(t_entry)).ldap_entry(dict(search_base=(ldap_url.dn),
              owner=(owner.dn_s),
              serial=yk_serial))
            token_dn = ','.join((token_dn, ldap_url.dn))
            oath_ldap.add_s(token_dn, token_entry)
            cli_output('Added OATH-LDAP entry %r' % token_dn)
            oath_ldap.unbind_s()
    except USBError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except ldap0.ALREADY_EXISTS:
        cli_output('Entry %r already exists!' % token_dn)
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