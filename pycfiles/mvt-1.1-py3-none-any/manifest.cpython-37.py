# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/manifest.py
# Compiled at: 2020-02-21 08:16:28
# Size of source mod 2**32: 2794 bytes
import io, os, sqlite3, operator, logging, biplist
from .base import IOSExtraction
from ..utils import convert_timestamp_to_iso
log = logging.getLogger(__name__)

class Manifest(IOSExtraction):
    __doc__ = 'This module extracts information from a backup Manifest.db file.'
    enabled = False

    def run(self):
        manifest_db_path = os.path.join(self.base_folder, 'Manifest.db')
        log.info('Found Manifest.db database at path: %s', manifest_db_path)
        conn = sqlite3.connect(manifest_db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Files;')
        names = [description[0] for description in cur.description]
        files = []
        for file_entry in cur:
            file_data = dict()
            for index, value in enumerate(file_entry):
                file_data[names[index]] = value

            cleaned_metadata = {'fileID':file_data['fileID'], 
             'domain':file_data['domain'], 
             'relativePath':file_data['relativePath'], 
             'flags':file_data['flags'], 
             'created':''}
            if file_data['file']:
                file_plist = biplist.readPlist(io.BytesIO(file_data['file']))
                file_metadata = file_plist[b'$objects'][1]
                cleaned_metadata.update({'created':convert_timestamp_to_iso(file_metadata[b'Birth']), 
                 'modified':convert_timestamp_to_iso(file_metadata[b'LastModified']), 
                 'statusChanged':convert_timestamp_to_iso(file_metadata[b'LastStatusChange']), 
                 'mode':oct(file_metadata[b'Mode']), 
                 'owner':file_metadata[b'UserID'], 
                 'size':file_metadata[b'Size']})
            files.append(cleaned_metadata)

        cur.close()
        conn.close()
        log.info('Extracted a total of %d file metadata items', len(files))
        self.results = files