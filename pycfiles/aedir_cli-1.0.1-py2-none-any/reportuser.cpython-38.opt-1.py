# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_cli/reportuser.py
# Compiled at: 2020-03-29 12:38:38
# Size of source mod 2**32: 2001 bytes
"""
Generates a report of active aeUser entries and their aePerson attributes
"""
import sys, csv, ldap0, aedir
from .reportperson import AEPERSON_ATTRS
AEUSER_ATTRS = [
 'aePerson',
 'uid',
 'uidNumber',
 'entryUUID',
 'aeTicketId',
 'description',
 'memberOf',
 'aeNotBefore',
 'aeNotAfter',
 'pwdChangedTime',
 'createTimestamp',
 'modifyTimestamp']
VIRTUAL_ATTRS = [
 'aeZoneName']

def main():
    with aedir.AEDirObject(None, cache_ttl=1800.0) as (ldap_conn):
        aedir_search_base = ldap_conn.search_base
        msg_id = ldap_conn.search(aedir_search_base,
          (ldap0.SCOPE_SUBTREE),
          '(&(objectClass=aeUser)(aeStatus=0))',
          attrlist=AEUSER_ATTRS)
        column_attrs = AEUSER_ATTRS + AEPERSON_ATTRS + VIRTUAL_ATTRS
        csv_writer = csv.DictWriter((sys.stdout), column_attrs, dialect='excel')
        csv_writer.writerow({at:at for at in column_attrs})
        for res in ldap_conn.results(msg_id):
            for result in res.rdata:
                user_dn = result.dn_s
                user_entry = result.entry_s
                user_entry['aeZoneName'] = [
                 aedir.extract_zone(user_dn, aeroot_dn=aedir_search_base)]
                person_result = ldap_conn.read_s((user_entry['aePerson'][0]), attrlist=AEPERSON_ATTRS)
                user_entry.update(person_result.entry_s)
                user_dict = {'|'.join(av):at for at, av in user_entry.items()}
                csv_writer.writerow(user_dict)


if __name__ == '__main__':
    main()