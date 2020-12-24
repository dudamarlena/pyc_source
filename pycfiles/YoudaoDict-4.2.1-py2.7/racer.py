# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/racer.py
# Compiled at: 2019-02-16 23:51:48
import sys
from gevent.monkey import patch_all
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore
from gevent.timeout import Timeout
from youdao.spider import Spider
from youdao.customizer import Customize
from youdao.sqlsaver import SQLSaver
patch_all()
reload(sys)
sys.setdefaultencoding('utf8')

class Race(object):

    def __init__(self, phrase=''):
        self.phrase = phrase.lower()
        self.pool = Pool()
        self.sem = BoundedSemaphore(3)
        self.result = None
        self.sql_saver = SQLSaver()
        return

    def race(self, runner):
        """
        let runners run for themselves
        :param runner: callable runner
        """
        with self.sem:
            try:
                runner()
            except Timeout:
                pass

    def local_sql_fetch(self):
        """fetch local cache from sqlite"""
        with Timeout(1, False):
            result = self.sql_saver.query(self.phrase)
            if result:
                self.racer_weapon(result, gun='sql')

    def custom_server_fetch(self):
        """fetch result from customer server"""
        with Timeout(5, False):
            result = Customize(self.phrase).server_fetch()
            if result:
                self.racer_weapon(result, gun='custom')

    def official_server_fetch(self):
        """fetch result from official site"""
        timeout = 7
        with Timeout(timeout, False):
            _, result = Spider(timeout=timeout).deploy(self.phrase)
            if result:
                self.racer_weapon(result, gun='official')

    def racer_weapon(self, bullet, gun):
        """
        bullet to stop the race
        :param bullet: result for the game
        :param gun: winner name
        :return:
        """
        self.result = bullet
        if not gun == 'sql' and 'possibles' not in bullet:
            self.sql_saver.upset(self.phrase, bullet)
        self.pool.kill()

    def launch_race(self):
        """start race"""
        self.pool.map(self.race, [
         self.custom_server_fetch,
         self.official_server_fetch,
         self.local_sql_fetch])