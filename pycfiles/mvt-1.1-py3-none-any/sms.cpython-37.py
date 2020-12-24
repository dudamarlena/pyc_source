# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/sms.py
# Compiled at: 2020-02-21 08:16:28
# Size of source mod 2**32: 3143 bytes
import os, sqlite3, logging
from base64 import b64encode
from .base import IOSExtraction
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso, check_for_links
log = logging.getLogger(__name__)
SMS_BACKUP_ID = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
SMS_ROOT_PATHS = [
 'private/var/mobile/Library/SMS/sms.db']

class SMS(IOSExtraction):
    __doc__ = 'This module extracts all SMS messages containing links.'

    def run(self):
        self._find_database(backup_id=SMS_BACKUP_ID, root_paths=SMS_ROOT_PATHS)
        log.info('Found SMS database at path: %s', self.file_path)
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n                message.*,\n                handle.id as "phone_number"\n            FROM message, handle\n            WHERE handle.rowid = message.handle_id;')
        names = [description[0] for description in cur.description]
        messages = []
        for message in cur:
            new_message = dict()
            for index, value in enumerate(message):
                if not names[index] == 'attributedBody':
                    if names[index] == 'payload_data':
                        if value:
                            value = b64encode(value).decode('utf-8')
                    new_message[names[index]] = value

            new_message['isodate'] = convert_timestamp_to_iso(convert_mactime_to_unix(new_message['date']))
            new_message['direction'] = 'sent' if new_message['is_from_me'] == 1 else 'received'
            message_links = check_for_links(new_message['text'])
            if message_links:
                if self.domains:
                    self._check_domains(message_links)
            if message_links or new_message['text'].strip() == '':
                messages.append(new_message)

        cur.close()
        conn.close()
        log.info('Extracted a total of %d SMS messages containing links', len(messages))
        self.results = messages