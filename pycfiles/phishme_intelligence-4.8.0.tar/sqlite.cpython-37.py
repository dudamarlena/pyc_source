# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/core/sqlite.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 4934 bytes
from __future__ import unicode_literals, absolute_import
import json, logging, sys, sqlite3
PYTHON_MAJOR_VERSION = sys.version_info[0]

class SQLite(object):
    __doc__ = '\n\n    '

    def __init__(self, location, data_retention_days):
        """
        Initialize a SQLite object

        :param str location: Filesystem location to write SQLite database to
        :param int data_retention_days: Number of days to retain data in SQLite database
        """
        self.db_location = location
        self.data_retention_days = data_retention_days
        self.logger = logging.getLogger(__name__)
        self.updated_threat_intel = False
        self.con = sqlite3.connect(self.db_location)
        with self.con:
            cur = self.con.cursor()
            cur.execute('\n                CREATE TABLE IF NOT EXISTS threats(\n                    threat_type TEXT,\n                    threat_id INTEGER,\n                    last_modified INTEGER,\n                    json TEXT,\n                    revision INTEGER DEFAULT 1,\n                    UNIQUE(threat_type, threat_id) ON CONFLICT REPLACE\n                )\n                ')
        self.updated_threat_intel = self._apply_retention()

    def add_threat_id(self, intel):
        """
        Add PhishMe Intelligence Threat ID data to SQLite database

        :param intel: PhishMe Intelligence Threat ID data object
        :type intel: :class:`phishme_intelligence.core.intelligence.Malware`
        :return: None
        """
        with self.con:
            cur = self.con.cursor()
            sql_insert_threat = 'INSERT INTO threats\n                                    (threat_type, threat_id, last_modified, json, revision)\n                                VALUES\n                                    (:threat_type, :threat_id, :last_modified, :json, (COALESCE((SELECT revision FROM threats WHERE threat_type="malware" AND threat_id=:threat_id), 0) + 1)\n                                )'
            values = {'threat_type':'malware', 
             'threat_id':intel.threat_id, 
             'last_modified':intel.last_published, 
             'json':json.dumps(intel.json)}
            cur.execute(sql_insert_threat, values)

    def get_threats(self):
        """
        Generator method to return Threat ID JSON data from SQLite database

        :return: (generator) Threat ID JSON data
        :rtype: dict
        """
        with self.con:
            dummy = self.con.cursor()
            for result in self.con.execute('SELECT threat_id, json, revision FROM threats WHERE threat_type = "malware" ORDER BY threat_id'):
                json_data = json.loads(result[1])
                yield json_data

    def _apply_retention(self):
        """
        Delete all items in SQLite database outside retention policy.

        :return: Whether or not rows were deleted
        :rtype: bool
        """
        rows_deleted = self.con.execute('DELETE FROM threats WHERE datetime(last_modified / 1000, "unixepoch") < datetime("now", "-' + str(self.data_retention_days) + ' day")').rowcount
        self.logger.info('Deleted ' + str(rows_deleted) + ' Threat IDs from sqlite db over ' + str(self.data_retention_days) + ' days old.')
        self.con.execute('VACUUM')
        if rows_deleted > 0:
            return True
        return False