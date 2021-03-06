# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/livedata.py
# Compiled at: 2020-04-11 12:14:12
# Size of source mod 2**32: 8587 bytes
import time, logging, threading
from difflib import SequenceMatcher
from ComunioScore.dbhandler import DBHandler
from ComunioScore.matchscheduler import MatchScheduler
from ComunioScore.score.bundesligascore import BundesligaScore
from ComunioScore.messenger.comunioscore_telegram import ComunioScoreTelegram

class LiveDataProvider(DBAgent):
    __doc__ = ' class LiveDataProvider to trigger matches for providing livedata\n\n    USAGE:\n            livedata = LiveDataProvider()\n            livedata.start()\n\n    '

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('create class LiveDataProvider')
        super().__init__(config_file='cfg.ini')
        self.scheduler = MatchScheduler()
        self._LiveDataProvider__thread = threading.Thread(target=(self._LiveDataProvider__run))
        self._LiveDataProvider__running = False

    def __del__(self):
        pass

    def start(self, daemon=False):
        """ starts the run thread for LiveDataProvider

        """
        if self._LiveDataProvider__thread:
            if isinstance(daemon, bool):
                self._LiveDataProvider__thread.daemon = daemon
                self._LiveDataProvider__running = True
                self.logger.info('start the LiveDataProvider run thread')
                self._LiveDataProvider__thread.start()
            else:
                raise TypeError("'daemon' must be type of boolean")

    def stop(self):
        """ stops the run thread for LiveDataProvider

        """
        if self._LiveDataProvider__thread:
            self._LiveDataProvider__running = False
            self.logger.info('stop the LiveDataProvider run thread')
            self._LiveDataProvider__thread.join()

    def trigger_matches(self):
        """ triggers new match events from database

        """
        sql = "select * from comunioscore.season where match_type='notstarted' order by start_timestamp asc"
        matches = self.dbfetcher.many(sql=sql, size=9)
        for match in matches:
            self.logger.info('register matchid {} for {} : {}'.format(match[2], match[5], match[6]))
            self.scheduler.register_events(match[3], self.execute, 1, match[0], match[2], match[5], match[6])

    def execute(self, matchday, matchid, hometeam, awayteam):
        """ executes the match event

        """
        fetcher = LiveDataFetcher(matchday=matchday, matchid=matchid, hometeam=hometeam, awayteam=awayteam)
        fetcher.start()

    def __run(self):
        """ run thread to trigger the match events

        """
        while self._LiveDataProvider__running:
            self.logger.info('trigger matches')
            self.trigger_matches()
            while not self.scheduler.is_queue_empty():
                self.scheduler.run(blocking=False)

            time.sleep(600)


class LiveDataFetcher(BundesligaScore, threading.Thread, DBAgent):
    __doc__ = ' class LiveDataFetcher to fetch live data from sofascore\n\n    USAGE:\n            livefetcher = LiveDataFetcher()\n            livefetcher.start()\n\n    '

    def __init__(self, matchday, matchid, hometeam, awayteam):
        BundesligaScore.__init__(self)
        threading.Thread.__init__(self)
        DBAgent.__init__(self, config_file='cfg.ini')
        self.matchday = matchday
        self.matchid = matchid
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.user_sql = 'select userid, username from comunioscore.communityuser'
        self.squad_sql = 'select username, playername, club from comunioscore.squad where userid = %s'
        self.comuniouser = self.dbfetcher.all(sql=(self.user_sql))
        self.telegram = ComunioScoreTelegram(token=(self.telegram_token))

    def run(self):
        """ run thread for lineup rating

        """
        start_msg = 'Start fetching live data from matchday {} with {} : {}'.format(self.matchday, self.hometeam, self.awayteam)
        self.logger.info(start_msg)
        self.telegram.new_msg(text=start_msg)
        while not self.is_finished(matchid=(self.matchid)):
            rest_data = self.create_rest_query()
            comunio_livedata = self.get_comunio_livedata(rest_query_list=rest_data)
            telegram_str = ''
            match_str = 'Match {} : {} \n\n'.format(self.hometeam, self.awayteam)
            telegram_str += match_str
            for user in comunio_livedata:
                for player in user['squad']:
                    player_str = ''.join('{}: {} {}\n'.format(user['user'], player['name'], player['rating']))
                    telegram_str += player_str

            self.logger.info(telegram_str)
            self.telegram.new_msg(text=telegram_str)
            time.sleep(540)

        finish_str = 'finished match {} : {}'.format(self.hometeam, self.awayteam)
        self.logger.info(finish_str)
        self.telegram.new_msg(text=finish_str)

    def create_rest_query(self):
        """ creates the rest query for sofascore data

        :return: list for the rest query
        """
        rest_query_list = list()
        for user in self.comuniouser:
            squad = self.dbfetcher.all(sql=(self.squad_sql), data=(user[0],))
            req_player = list()
            for player in squad:
                team = player[2]
                if team == self.hometeam or team == self.awayteam:
                    req_player.append(player)
                else:
                    hometeam_ratio = SequenceMatcher(None, team, self.hometeam).ratio()
                    awayteam_ratio = SequenceMatcher(None, team, self.awayteam).ratio()
                    if hometeam_ratio > 0.6 or awayteam_ratio > 0.6:
                        req_player.append(player)

            user_query = dict()
            user_query['user'] = user[1]
            user_query['req_squad'] = req_player
            rest_query_list.append(user_query)

        return rest_query_list

    def get_comunio_livedata(self, rest_query_list):
        """ get the parsed comunio livedata

        :return: list: comunio user specific data
        """
        lineup = self.lineup_from_match_id(self.matchid)
        comunio_livedata = list()
        for comuniouser in rest_query_list:
            user_squad_dict = dict()
            user_squad_dict['user'] = comuniouser['user']
            user_squad_dict['squad'] = list()
            for player in comuniouser['req_squad']:
                for homeplayer, awayplayer in zip(lineup['homeTeam'], lineup['awayTeam']):
                    homeplayer_surename = homeplayer['player_name'].split()[1]
                    awayplayer_surename = awayplayer['player_name'].split()[1]
                    if homeplayer_surename == player[1] or homeplayer['player_name'] == player[1]:
                        player_data = dict()
                        player_data['name'] = player[1]
                        player_data['rating'] = homeplayer['player_rating']
                        user_squad_dict['squad'].append(player_data)
                    else:
                        if awayplayer_surename == player[1] or awayplayer['player_name'] == player[1]:
                            player_data = dict()
                            player_data['name'] = player[1]
                            player_data['rating'] = awayplayer['player_rating']
                            user_squad_dict['squad'].append(player_data)
                        else:
                            homeplayer_ratio = SequenceMatcher(None, homeplayer_surename, player[1]).ratio()
                            awayplayer_ratio = SequenceMatcher(None, awayplayer_surename, player[1]).ratio()
                            if homeplayer_ratio > 0.6:
                                player_data = dict()
                                player_data['name'] = player[1]
                                player_data['rating'] = homeplayer['player_rating']
                            else:
                                if awayplayer_ratio > 0.6:
                                    player_data = dict()
                                    player_data['name'] = player[1]
                                    player_data['rating'] = awayplayer['player_rating']
                                    user_squad_dict['squad'].append(player_data)

            comunio_livedata.append(user_squad_dict)

        return comunio_livedata


if __name__ == '__main__':
    fetcher = LiveDataFetcher('8', matchid=8272023, hometeam='FC Schalke 04', awayteam='Hertha BSC')
    fetcher.start()