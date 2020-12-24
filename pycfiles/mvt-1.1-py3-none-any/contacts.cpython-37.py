# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/contacts.py
# Compiled at: 2020-02-21 08:16:28
# Size of source mod 2**32: 2131 bytes
import os, sqlite3, logging
from .base import IOSExtraction
log = logging.getLogger(__name__)
CONTACTS_BACKUP_ID = '31bb7ba8914766d4ba40d6dfb6113c8b614be442'
CONTACTS_ROOT_PATHS = [
 'private/var/mobile/Library/AddressBook/AddressBook.sqlitedb']

class Contacts(IOSExtraction):
    __doc__ = "This module extracts all contact details from the phone's address book."

    def run(self):
        self._find_database(backup_id=CONTACTS_BACKUP_ID, root_paths=CONTACTS_ROOT_PATHS)
        log.info('Found Contacts database at path: %s', self.file_path)
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n            multi.value, person.first, person.middle, person.last,\n            person.organization\n            FROM ABPerson person, ABMultiValue multi\n            WHERE person.rowid = multi.record_id and multi.value not null\n            ORDER by person.rowid ASC;')
        names = [description[0] for description in cur.description]
        contacts = []
        for entry in cur:
            new_contact = dict()
            for index, value in enumerate(entry):
                new_contact[names[index]] = value

            contacts.append(new_contact)

        cur.close()
        conn.close()
        log.info('Extracted a total of %d contacts from the address book', len(contacts))
        self.results = contacts