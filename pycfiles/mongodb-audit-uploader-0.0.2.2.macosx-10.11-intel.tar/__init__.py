# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benwaters/mongo-auditor/lib/python2.7/site-packages/mongodb_auditor_uploader/__init__.py
# Compiled at: 2016-09-01 08:47:18
from __future__ import print_function
from datetime import datetime, timedelta
from os.path import expanduser, join, isfile
import ConfigParser, json
from elasticsearch import Elasticsearch, ElasticsearchException

class MongoAuditUploader(object):
    CONFIG_PATH = '/etc/default/mongodb-audit-uploader'

    def setup(self):
        """

        :return:
        """
        if not isfile(self.CONFIG_PATH):
            config_file = open(self.CONFIG_PATH, 'w')
            config = ConfigParser.SafeConfigParser()
            config.set(ConfigParser.DEFAULTSECT, 'audit_log_location', join(expanduser('~'), 'audit.json'))
            config.write(config_file)
            config_file.close()

    def load_config(self):
        """

        :return:
        """
        if self.config_path == self.CONFIG_PATH:
            parser = ConfigParser.SafeConfigParser()
            parser.read(self.CONFIG_PATH)
            self.days = int(parser.get(ConfigParser.DEFAULTSECT, 'days'))
            self.start_date = self.today - timedelta(days=self.days)
            self.structure['start_date'] = str(self.start_date)
            self.elasticsearch_host = parser.get(ConfigParser.DEFAULTSECT, 'elasticsearch_host')
            self.elasticsearch_port = parser.get(ConfigParser.DEFAULTSECT, 'elasticsearch_port')
            self.audit_log_location = parser.get(ConfigParser.DEFAULTSECT, 'audit_log_location')

    def parse_file(self):
        """

        :return:
        """
        with open(self.audit_log_location, 'r+') as (audit_file):
            for entry in audit_file:
                entry = json.loads(entry)
                if len(entry.get('users')) == 0:
                    continue
                else:
                    user = entry.get('users')[0].get('user')
                    action = entry.get('atype')
                    if action == 'authenticate' and entry.get('result') != 0:
                        action = 'INVALID authenticate'
                    timestamp = datetime.utcfromtimestamp(int(entry.get('ts').get('$date').get('$numberLong')) / 1000.0)
                    if (self.today - timestamp).days < int(self.days):
                        if user in self.structure['users'].keys():
                            if action in self.structure['users'][user].keys():
                                self.structure['users'][user][action] += 1
                            else:
                                self.structure['users'][user][action] = 1
                        else:
                            self.structure['users'][user] = {action: 1}
                    else:
                        continue

    def upload(self):
        """

        :return:
        """
        es = Elasticsearch([{'host': self.elasticsearch_host, 'port': self.elasticsearch_port}])
        index = ('mongodb-audit-{}-{}-{}').format(self.today.month, self.today.day, self.today.year)
        for user in self.structure['users']:
            try:
                es.index(index=index, doc_type='mongodb-audit', body={'user': user, 'actions': self.structure['users'][user], 'timestamp': str(self.today.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))}, timestamp=self.today)
            except ElasticsearchException as msg:
                print(msg)

    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config = None
        self.days = 0
        self.elasticsearch_host = ''
        self.elasticsearch_port = ''
        self.audit_log_location = ''
        self.today = datetime.utcnow()
        self.start_date = None
        self.structure = {'users': {}}
        self.setup()
        self.load_config()
        self.parse_file()
        self.upload()
        return