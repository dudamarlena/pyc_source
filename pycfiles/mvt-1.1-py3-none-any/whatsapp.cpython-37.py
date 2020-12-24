# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/whatsapp.py
# Compiled at: 2020-02-21 08:16:28
# Size of source mod 2**32: 2717 bytes
import os, sqlite3, logging
from .base import IOSExtraction
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso, check_for_links
log = logging.getLogger(__name__)
WHATSAPP_BACKUP_ID = '7c7fba66680ef796b916b067077cc246adacf01d'
WHATSAPP_ROOT_PATHS = [
 'private/var/mobile/Containers/Shared/AppGroup/*/ChatStorage.sqlite']

class Whatsapp(IOSExtraction):
    __doc__ = 'This module extracts all WhatsApp messages containing links.'

    def run(self):
        self._find_database(backup_id=WHATSAPP_BACKUP_ID, root_paths=WHATSAPP_ROOT_PATHS)
        log.info('Found WhatsApp database at path: %s', self.file_path)
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM ZWAMESSAGE;')
        names = [description[0] for description in cur.description]
        messages = []
        for message in cur:
            new_message = dict()
            for index, value in enumerate(message):
                new_message[names[index]] = value

            if not new_message['ZTEXT']:
                continue
            new_message['isodate'] = convert_timestamp_to_iso(convert_mactime_to_unix(new_message['ZMESSAGEDATE']))
            message_links = check_for_links(new_message['ZTEXT'])
            if message_links:
                if self.domains:
                    self._check_domains(message_links)
            if not new_message['ZTEXT'] or message_links or new_message['ZTEXT'].strip() == '':
                messages.append(new_message)

        cur.close()
        conn.close()
        log.info('Extracted a total of %d WhatsApp messages containing links', len(messages))
        self.results = messages