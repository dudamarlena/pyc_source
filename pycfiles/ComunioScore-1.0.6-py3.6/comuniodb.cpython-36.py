# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/comuniodb.py
# Compiled at: 2020-04-27 15:29:14
# Size of source mod 2**32: 8737 bytes
import logging, datetime
from threading import Thread
from time import sleep, time
from ComunioScore import DBHandler
from ComunioScore import Comunio
from ComunioScore.exceptions import DBInserterError

class ComunioDB(DBHandler, Thread):
    __doc__ = " class ComunioDB to insert comunio data into database\n\n    USAGE:\n            comuniodb = ComunioDB(comunio_user='', comunio_pass='', update_frequence=21600, **dbparams)\n            comuniodb.start()\n\n    "

    def __init__(self, comunio_user, comunio_pass, update_frequence=21600, **dbparams):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class ComunioDB')
        (DBHandler.__init__)(self, **dbparams)
        Thread.__init__(self)
        self.comunio_username = comunio_user
        self.comunio_password = comunio_pass
        self.update_frequence = update_frequence
        self.comunio = Comunio()
        self.running = True
        self.player_standings = None

    def run(self) -> None:
        """ run thread for class ComunioDB

        """
        self._ComunioDB__comunio_login()
        self.delete_comunio_user()
        self.delete_squad()
        sleep(1)
        self.insert_comunio_user()
        self.insert_squad()
        self.logger.info('Start comuniodb run thread!')
        while self.running:
            sleep(self.update_frequence)
            self._ComunioDB__comunio_login()
            self.update_comunio_user()
            self.update_squad()

    def __comunio_login(self):
        """ tries to login to comunio

        """
        while not self.comunio.login(username=(self.comunio_username), password=(self.comunio_password)):
            self.logger.error('Could not login to comunio, wait 120s')
            sleep(120)

    def insert_comunio_user(self):
        """ insert comunio user into database

        """
        self.logger.info('Insert comunio {} data into database'.format(self.comunioscore_table_user))
        comuniouser = list()
        self.player_standings = self.comunio.get_player_standings()
        communityname = self.comunio.get_community_name()
        for player in self.player_standings:
            comuniouser.append((player['id'], player['name'].strip(), communityname, player['points'], player['teamValue']))

        sql = 'insert into {}.{} (userid, username, community, points, teamvalue) values(%s, %s, %s, %s, %s)'.format(self.comunioscore_schema, self.comunioscore_table_user)
        try:
            self.dbinserter.many_rows(sql=sql, datas=comuniouser)
        except DBInserterError as ex:
            self.logger.error(ex)

    def update_comunio_user(self):
        """ updates comunio user in the database

        """
        self.logger.info('Updating comunio {} data in database'.format(self.comunioscore_table_user))
        self.player_standings = self.comunio.get_player_standings()
        communityname = self.comunio.get_community_name()
        sql = 'update {}.{} set username = %s, community = %s, points = %s, teamvalue = %s where userid = %s'.format(self.comunioscore_schema, self.comunioscore_table_user)
        try:
            for player in self.player_standings:
                self.dbinserter.row(sql=sql, data=(player['name'].strip(), communityname, player['points'], player['teamValue'],
                 player['id']))

        except DBInserterError as ex:
            self.logger.error(ex)

    def delete_comunio_user(self):
        """ deletes comunio user data from database

        """
        self.logger.info('Deleting {} data from database'.format(self.comunioscore_table_user))
        sql = 'delete from {}.{}'.format(self.comunioscore_schema, self.comunioscore_table_user)
        try:
            self.dbinserter.sql(sql=sql)
        except DBInserterError as ex:
            self.logger.error(ex)

    def insert_squad(self):
        """ inserts squad data into database

        """
        self.logger.info('Insert {} data into database'.format(self.comunioscore_table_squad))
        users = self.comunio.get_comunio_user_data()
        sql = 'insert into {}.{} (userid, username, playername, playerposition, club, linedup) values(%s, %s, %s, %s, %s, %s)'.format(self.comunioscore_schema, self.comunioscore_table_squad)
        try:
            for user in users:
                for player in user['squad']:
                    self.dbinserter.row(sql=sql, data=(user['id'], user['name'], player['name'], player['position'],
                     player['club'], player['linedup']),
                      autocommit=True)

        except DBInserterError as ex:
            self.logger.error(ex)

    def update_squad(self):
        """ updates the squad data from comunio user

        """
        self.logger.info('Updating {} data'.format(self.comunioscore_table_squad))
        users = self.comunio.get_comunio_user_data()
        sql = 'insert into {}.{} (userid, username, playername, playerposition, club, linedup) values(%s, %s, %s, %s, %s, %s)'.format(self.comunioscore_schema, self.comunioscore_table_squad)
        try:
            for user in users:
                self.dbinserter.sql(sql=('delete from {}.{} where userid = {}'.format(self.comunioscore_schema, self.comunioscore_table_squad, int(user['id']))))
                for player in user['squad']:
                    self.dbinserter.row(sql=sql, data=(user['id'], user['name'], player['name'], player['position'], player['club'], player['linedup']))

        except DBInserterError as ex:
            self.logger.error(ex)

    def delete_squad(self):
        """ deletes squad data from database

        """
        self.logger.info('Deleting {} data from database'.format(self.comunioscore_table_squad))
        sql = 'truncate {}.{}'.format(self.comunioscore_schema, self.comunioscore_table_squad)
        try:
            self.dbinserter.sql(sql=sql, autocommit=True)
        except DBInserterError as ex:
            self.logger.error(ex)

    def insert_auth(self):
        """ insert comunio auth data into database

        """
        self.logger.info('Insert auth data into database')
        ts_utc = int(str(time()).split('.')[0])
        dt = str(datetime.datetime.now())
        auth = self.comunio.get_auth_info()
        exp_ts_utc = int(str(time()).split('.')[0]) + int(auth['expires_in'])
        exp_dt = datetime.datetime.fromtimestamp(exp_ts_utc)
        sql = 'insert into {}.auth (timestamp_utc, datetime, expires_in, expire_timestamp_utc, expire_datetime, access_token, token_type, refresh_token) values (%s, %s, %s, %s, %s, %s, %s, %s)'.format(self.comunioscore_schema)
        try:
            self.dbinserter.row(sql=sql, data=(ts_utc, dt, auth['expires_in'], exp_ts_utc, exp_dt, auth['access_token'],
             auth['token_type'], auth['refresh_token']))
        except DBInserterError as ex:
            self.logger.error(ex)

    def delete_auth(self):
        """ deletes the auth entries from database

        """
        self.logger.info('Deleting auth data from database')
        sql = 'delete from {}.auth'.format(self.comunioscore_schema)
        try:
            self.dbinserter.sql(sql=sql)
        except DBInserterError as ex:
            self.logger.error(ex)

    def get_comunio_user_data(self):
        """ get comunio user data

        :return: dict with comunio user data
        """
        return self.player_standings

    def update_linedup_squad(self):
        """ updates linedup squad in database

        """
        self.logger.info('Updating linedup squad data')
        user_sql = 'select userid from {}.{}'.format(self.comunioscore_schema, self.comunioscore_table_user)
        linedup_sql = 'update {}.{} set linedup = %s where userid = %s and playername = %s'.format(self.comunioscore_schema, self.comunioscore_table_squad)
        comunio_users = self.dbfetcher.all(sql=user_sql)
        for user in comunio_users:
            userid = user[0]
            squad = self.comunio.get_squad(userid=userid)
            for player in squad:
                playername = player['name']
                linedup = player['linedup']
                try:
                    self.dbinserter.row(sql=linedup_sql, data=(linedup, userid, playername))
                except DBInserterError as ex:
                    self.logger.error(ex)