# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_cli/reportperson.py
# Compiled at: 2020-03-29 12:22:56
# Size of source mod 2**32: 1892 bytes
"""
Generates a report of aePerson entries referenced by active aeUser entries
"""
import sys, csv, ldap0
from ldap0.controls.deref import DereferenceControl
import aedir
USER_ATTRS = [
 '1.1']
AEPERSON_ATTRS = [
 'sn',
 'givenName',
 'cn',
 'mail',
 'employeeNumber',
 'employeeType',
 'telephoneNumber',
 'mobile',
 'homePhone',
 'aeDept',
 'ou',
 'departmentNumber',
 'o',
 'street',
 'l',
 'c']
DEREF_CONTROL = DereferenceControl(True, {'aePerson': AEPERSON_ATTRS})

def main():
    person_dict = {}
    with aedir.AEDirObject(None, cache_ttl=1800.0) as (ldap_conn):
        msg_id = ldap_conn.search((ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          '(&(objectClass=aeUser)(aeStatus=0))',
          attrlist=USER_ATTRS,
          req_ctrls=[
         DEREF_CONTROL])
        for res in ldap_conn.results(msg_id):
            for result in res.rdata:
                if result.ctrls and result.ctrls[0].controlType == DereferenceControl.controlType:
                    deref_control = result.ctrls[0]
                    person_dict[deref_control.derefRes['aePerson'][0].dn_s.lower()] = dict([(
                     at, '|'.join(av)) for at, av in deref_control.derefRes['aePerson'][0].entry_s.items()])

    csv_writer = csv.DictWriter((sys.stdout),
      AEPERSON_ATTRS,
      dialect='excel')
    csv_writer.writerow(dict([(
     at, at) for at in AEPERSON_ATTRS]))
    csv_writer.writerows(person_dict.values())


if __name__ == '__main__':
    main()