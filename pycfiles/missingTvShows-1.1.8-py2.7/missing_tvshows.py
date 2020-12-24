# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/Kodi/missing_tvshows.py
# Compiled at: 2016-01-08 04:46:41
from __future__ import unicode_literals
from pytvdbapi import api
from colorama import Fore, Back, Style
from sqlalchemy import create_engine, Table, MetaData, func
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, REAL
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy.orm import mapper
from os.path import expanduser, join
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
import sqlite3, sys, os, shutil, logging, logging.config, argparse, time, math, random, signal, csv
if float(sys.version[:3]) < 3.0:
    import ConfigParser
else:
    import configparser as ConfigParser

class TVShows():

    def __init__(self):
        """Do some initialization stuff"""
        self.original_sigint = signal.getsignal(signal.SIGINT)
        self.__CONFIG_DIR = b'/etc/MissingTVShows/'
        self.__USER_CONFIG_DIR = expanduser(b'~/.MissingTVShows')
        self._checkUserConfigFiles()
        logging.basicConfig(level=logging.ERROR)
        logging.config.fileConfig([
         join(self.__USER_CONFIG_DIR, b'logging.conf'), expanduser(b'~/.logging.conf'), b'logging.conf'], defaults={b'logfilename': os.path.join(expanduser(b'~/.MissingTVShows'), b'tvshows.log')})
        self.__log = logging.getLogger(b'TVShows')
        if float(sys.version[:3]) < 3.2:
            config = ConfigParser.SafeConfigParser()
        else:
            config = ConfigParser.ConfigParser()
        config.read([join(self.__USER_CONFIG_DIR, b'tvshows.cfg'), expanduser(b'~/.tvshows.cfg'), b'tvshows.cfg'])
        self.__cwd = os.getcwd()
        self.__forceUpdate = False
        self.__forceLocal = False
        self.__produceCVS = False
        self.__totalOfSeriesSeason = 0
        self.__alreadyCheckedSeriesSeason = 0
        self.__random = random.SystemRandom(time.localtime())
        self.__tvdbdatabse = join(self.__USER_CONFIG_DIR, config.get(b'Config', b'tvdbdb'))
        self.__api_key = config.get(b'Config', b'api_key')
        self.__dbdialect = config.get(b'Database', b'dialect')
        self.__database = config.get(b'Database', b'db')
        self.__dbuser = config.get(b'Database', b'user')
        self.__dbpasswd = config.get(b'Database', b'passwd')
        self.__dbhostname = config.get(b'Database', b'hostname')
        self.__dbport = config.get(b'Database', b'port')
        self.__log.debug(b'Database ' + self.__database)
        self.checkLocalTVDBDatabase()

    def _checkUserConfigFiles(self):
        if not os.path.exists(self.__USER_CONFIG_DIR):
            os.mkdir(self.__USER_CONFIG_DIR)
        if not os.path.exists(join(self.__USER_CONFIG_DIR, b'logging.conf')):
            shutil.copy(join(self.__CONFIG_DIR, b'logging.conf'), join(self.__USER_CONFIG_DIR, b'logging.conf'))
        if not os.path.exists(join(self.__USER_CONFIG_DIR, b'tvshows.cfg')):
            shutil.copy(join(self.__CONFIG_DIR, b'tvshows.cfg'), join(self.__USER_CONFIG_DIR, b'tvshows.cfg'))

    def _initDB(self):
        db_connection_string = b''
        try:
            if self.__dbdialect == b'mysql':
                db_connection_string = b'mysql://' + self.__dbuser + b':' + self.__dbpasswd + b'@' + self.__dbhostname + b':' + self.__dbport + b'/' + self.__database
            elif self.__dbdialect == b'sqlite':
                db_connection_string = b'sqlite:///' + self.__database
                if not self._isSQLite3(self.__database):
                    raise ValueError(self.__database + b' is not a valid sqlite database')
            if not database_exists(db_connection_string):
                raise ValueError(b'Database does not exist')
            engine = create_engine(db_connection_string)
            self.__log.debug(b'Connected to database ' + self.__database)
        except ProgrammingError:
            self.__log.error(b'Connection to database ' + self.__database + b' failed')
            raise ValueError(b'Could not connect to ' + db_connection_string)

        session = sessionmaker(bind=engine)
        self.__session = session()
        metaData = MetaData()
        metaData.bind = engine
        self.__tvshow = Table(b'tvshow', metaData, autoload=True)
        self.__seasons = Table(b'seasons', metaData, autoload=True)
        self.__episodeview = Table(b'episode_view', metaData, autoload=True)

    def _isSQLite3(self, filename):
        """Courtes of http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists"""
        from os.path import isfile, getsize
        if not isfile(filename):
            return False
        if getsize(filename) < 100:
            return False
        with open(filename, b'rb') as (f):
            header = f.read(100)
        return header[0:16] == b'SQLite format 3\x00'

    def _make_sql_queries(self):
        self._initDB()
        session = self.__session
        tvshow = self.__tvshow
        seasons = self.__seasons
        episodeview = self.__episodeview
        query = session.query(tvshow.c.c00.label(b'Title'), episodeview.c.c12.label(b'Season'), func.count().label(b'Episodes'), tvshow.c.c12.label(b'SeriesID'), episodeview.c.idSeason.label(b'SeasoniD'), func.sum(episodeview.c.playCount).label(b'Played')).select_from(episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason).join(tvshow, tvshow.c.idShow == seasons.c.idShow)).group_by(b'Title', b'Season').order_by(b'Title').having(func.sum(episodeview.c.playCount) == None)
        nonewatched = query.all()
        query = session.query(tvshow.c.c00.label(b'Title'), episodeview.c.c12.label(b'Season'), func.count().label(b'Episodes'), tvshow.c.c12.label(b'SeriesID'), episodeview.c.idSeason.label(b'SeasoniD'), func.sum(episodeview.c.playCount).label(b'Played')).select_from(episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason).join(tvshow, tvshow.c.idShow == seasons.c.idShow)).group_by(b'Title', b'Season').order_by(b'Title').having(func.sum(episodeview.c.playCount) > 0)
        somewatched = query.all()
        self.__totalOfSeriesSeason = len(nonewatched) + len(somewatched)
        return (nonewatched, somewatched)

    def _get_Episodes(self, season, seriesId):
        session = self.__session
        tvshow = self.__tvshow
        seasons = self.__seasons
        episodeview = self.__episodeview
        query = session.query(tvshow.c.c00.label(b'Title'), episodeview.c.c12.label(b'Season'), episodeview.c.c13.label(b'Episode'), tvshow.c.c12.label(b'SeriesID')).select_from(episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason).join(tvshow, tvshow.c.idShow == seasons.c.idShow)).filter(episodeview.c.c12 == season, tvshow.c.c12 == seriesId).order_by(b'Title', b'Season', b'Episode')
        episodes = query.all()
        return episodes

    def getTotalNumberOfEpisodes(self, series_id, season):
        engine = create_engine(b'sqlite:///' + self.__tvdbdatabse)
        sessionma = sessionmaker(bind=engine)
        session = sessionma()
        query = session.query(TVShow).filter_by(seriesid=series_id).filter_by(season=season)
        localshow = query.first()
        number_of_episodes = 0
        now = time.mktime(time.localtime())
        self.__alreadyCheckedSeriesSeason += 1
        progress = self.__alreadyCheckedSeriesSeason * 100 / self.__totalOfSeriesSeason
        sys.stdout.write(b'\r')
        sys.stdout.write(b'[%-100s] %d%%' % (b'=' * int(math.ceil(progress)), progress))
        sys.stdout.flush()
        self.__log.debug((b'Already done {:d} of {:d}').format(self.__alreadyCheckedSeriesSeason, self.__totalOfSeriesSeason))
        if not localshow and not self.__forceLocal:
            show = self.__db.get_series(series_id, b'en')
            number_of_episodes = len(show[season])
            next_update_time = now + self.__random.randint(0, 302400)
            self.__log.debug(b'Next update time is: ' + str(next_update_time))
            newlocalshow = TVShow(seriesid=series_id, season=season, totalnumofepisodes=number_of_episodes, lastupdated=next_update_time)
            session.add(newlocalshow)
            session.commit()
        elif not localshow and self.__forceLocal:
            number_of_episodes = -1
        elif self.__forceUpdate or now - localshow.lastupdated > 604800 and not self.__forceLocal:
            show = self.__db.get_series(series_id, b'en')
            number_of_episodes = len(show[season])
            next_update_time = now + self.__random.randint(0, 302400)
            self.__log.debug(b'Next update time is: ' + str(next_update_time))
            localshow.totalnumofepisodes = number_of_episodes
            localshow.lastupdated = next_update_time
            session.commit()
        else:
            number_of_episodes = localshow.totalnumofepisodes
        session.close()
        return number_of_episodes

    def checkLocalTVDBDatabase(self):
        con = sqlite3.connect(self.__tvdbdatabse)
        cur = con.cursor()
        cur.execute(b"Select name from sqlite_master where type='table';")
        if not cur.fetchall():
            cur = con.cursor()
            cur.execute(b'CREATE TABLE THETVDB (id INTEGER PRIMARY KEY, seriesid INTEGER, season INTEGER, totalnumofepisodes INTEGER, lastupdated REAL)')
            con.commit()
        con.close()

    def getSeriesInformation(self):
        """The main function"""
        if not self.__forceLocal:
            self.__db = api.TVDB(self.__api_key)
        try:
            nonewatched, somewatched = self._make_sql_queries()
        except ValueError as ve:
            self.__log.error((b'Could not query database: {0}').format(str(ve)))
            sys.exit(-5)

        unwatched_finished_shows = []
        unwatched_unfinished_shows = []
        watchedsome_unfinished_shows = []
        watchedsome_finished_shows = []
        for row in nonewatched:
            if int(row[1]) == 0:
                continue
            rowTitle = row[0]
            rowId = row[3]
            rowSeason = row[1]
            rowDownloaded = row[2]
            self.__log.debug((b'Currently treating series {:s} with id: {:s} and Season {:s}').format(rowTitle, rowId, rowSeason))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(rowId), int(rowSeason))
            full_episodes = range(1, number_of_episodes + 1)
            self.__log.debug((b'{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes').format(rowTitle, rowSeason, rowDownloaded, number_of_episodes))
            if int(number_of_episodes) != int(rowDownloaded):
                episodes = self._get_Episodes(rowSeason, rowId)
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])

                present_episodes = map(int, present_episodes)
                self.__log.debug(b'Present episodes ' + str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug(b'Missing episodes: ' + str(missing_episodes)[1:-1])
                unwatched_unfinished_shows.append({b'Title': rowTitle, b'SeasonId': rowId, b'Season': rowSeason, b'NbDownloaded': rowDownloaded, b'NbAvailable': number_of_episodes, b'NbWatched': 0, b'MissingEpisodes': str(missing_episodes)[1:-1]})
            else:
                unwatched_finished_shows.append({b'Title': rowTitle, b'SeasonId': rowId, b'Season': rowSeason, b'NbDownloaded': rowDownloaded, b'NbAvailable': number_of_episodes, b'NbWatched': 0, b'MissingEpisodes': 0})

        for row in somewatched:
            if int(row[1]) == 0:
                continue
            rowTitle = row[0]
            rowId = row[3]
            rowSeason = row[1]
            rowDownloaded = row[2]
            rowWatched = row[5]
            self.__log.debug((b'Currently treating series {:s} with id: {:s} and Season {:s}').format(rowTitle, rowId, rowSeason))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(rowId), int(rowSeason))
            full_episodes = range(1, number_of_episodes + 1)
            if int(number_of_episodes) != int(rowDownloaded):
                episodes = self._get_Episodes(rowSeason, rowId)
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])

                present_episodes = map(int, present_episodes)
                self.__log.debug(b'Present episodes: ' + str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug(b'Missing episodes: ' + str(missing_episodes)[1:-1])
                watchedsome_unfinished_shows.append({b'Title': rowTitle, b'SeasonId': rowId, b'Season': rowSeason, b'NbDownloaded': rowDownloaded, b'NbAvailable': number_of_episodes, b'NbWatched': rowWatched, b'MissingEpisodes': str(missing_episodes)[1:-1]})
            elif int(number_of_episodes) > rowWatched:
                watchedsome_finished_shows.append({b'Title': rowTitle, b'SeasonId': rowId, b'Season': rowSeason, b'NbDownloaded': rowDownloaded, b'NbAvailable': number_of_episodes, b'NbWatched': rowWatched, b'MissingEpisodes': 0})

        return (
         unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows)

    def _print_konsole(self, unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows):
        sys.stdout.write(b'\n')
        print Fore.RED + b'##############################################################'
        print b'###################### Unwatched Missing #####################'
        print b'##############################################################' + Style.RESET_ALL
        print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL
        print Style.DIM + Fore.GREEN + b'|' + Style.RESET_ALL + (b'{:44s} | {:s} ({:s}/{:s})| {:65s}|').format(b'Title', b'Season', b'Downloaded', b'Available', b'Missing')
        print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL
        for row in unwatched_unfinished_shows:
            print Style.DIM + Fore.GREEN + b'|' + Style.RESET_ALL + (b'{:43s}: | S{:2s} ({:2.0f}/{:2d})| missing: {:74s}|').format(row[b'Title'], row[b'Season'], row[b'NbDownloaded'], row[b'NbAvailable'], row[b'MissingEpisodes'])
            print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL

        print Fore.RED + b'###############################################################'
        print b'######################## Watched Missing ######################'
        print b'###############################################################' + Style.RESET_ALL
        print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL
        print Style.DIM + Fore.GREEN + b'|' + Style.RESET_ALL + (b'{:35s}({:8s})  | {:s} ({:s}/{:s})| {:65s}|').format(b'Title', b'SeasonId', b'Season', b'Downloaded', b'Available', b'Missing')
        print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL
        for row in watchedsome_unfinished_shows:
            print Style.DIM + Fore.GREEN + b'|' + Style.RESET_ALL + (b'{:35s}({:8s}): | S{:2s} ({:2.0f}/{:2d})| missing: {:74s}|').format(row[b'Title'], row[b'SeasonId'], row[b'Season'], row[b'NbDownloaded'], row[b'NbAvailable'], row[b'MissingEpisodes'])
            print Style.DIM + Fore.GREEN + b'-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL

        print Fore.RED + b'###############################################################'
        print b'######################## Ready to Watch #######################'
        print b'###############################################################' + Style.RESET_ALL
        for row in unwatched_finished_shows:
            print (b'{:35s}: Season {:2s} and has {:2.0f}/{:2d} Episodes').format(row[b'Title'], row[b'Season'], row[b'NbDownloaded'], row[b'NbAvailable'])

        print Fore.RED + b'###############################################################'
        print b'#################### Complete and Watching ####################'
        print b'###############################################################' + Style.RESET_ALL
        for row in watchedsome_finished_shows:
            print (b'{:35s}: Season {:2s} and has watched {:2.0f}/{:2d} Episodes').format(row[b'Title'], row[b'Season'], row[b'NbWatched'], row[b'NbDownloaded'])

    def _save_CSV(self, unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows):
        self._write_CSV(watchedsome_finished_shows, b'watchedsome_finished_shows.csv')
        self._write_CSV(unwatched_unfinished_shows, b'unwatched_unfinished_shows.csv')
        self._write_CSV(watchedsome_unfinished_shows, b'watchedsome_unfinished_shows.csv')

    def _write_CSV(self, series, filename):
        self.__log.debug(b'Writing to ' + filename)
        if sys.version_info >= (3, 0, 0):
            f = open(filename, b'w', newline=b'')
        else:
            f = open(filename, b'wb')
        with f:
            writer = csv.writer(f)
            writer.writerow([b'SeasonId', b'Title', b'Season', b'Downloaded', b'Available', b'Missing'])
            for show in series:
                writer.writerow([show[b'SeasonId'], show[b'Title'].encode(b'utf-8'), show[b'Season'], show[b'NbDownloaded'], show[b'NbAvailable'], show[b'MissingEpisodes']])

            f.close()

    def main(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        print b'Acquiring necessary TV-Shows information'
        unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows = self.getSeriesInformation()
        self._print_konsole(unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows)
        if self.__produceCVS:
            self._save_CSV(unwatched_finished_shows, unwatched_unfinished_shows, watchedsome_unfinished_shows, watchedsome_finished_shows)

    def getArguments(self, argv):
        if float(sys.version[:3]) < 3.0:
            self.__log.debug(b'Using Python 2')
        else:
            self.__log.debug(b'Using Python 3')
        parser = argparse.ArgumentParser(prog=b'missing_tvshows', description=b'Parsing the local XBMC library for TV-Shows and discovers if new episodes are availalbe', epilog=b'And that is how you use me')
        parser.add_argument(b'-i', b'--input', help=b'input sqlite database file', required=False, metavar=b'DATABASE')
        parser.add_argument(b'-f', b'--force-update', help=b'Force the update of the local TVDB Database', required=False, action=b'store_true', dest=b'forceupdate')
        parser.add_argument(b'-o', b'--offline', help=b'Force Offline mode, even if the script thinks that some entries needs to be refreshed', required=False, action=b'store_true', dest=b'forcelocal')
        parser.add_argument(b'-c', b'--csv', help=b'Produce CSV output files', required=False, action=b'store_true', dest=b'producecsv')
        args = parser.parse_args(argv)
        self.__database = args.input or self.__database
        self.__forceUpdate = args.forceupdate
        self.__forceLocal = args.forcelocal
        self.__produceCVS = args.producecsv
        if self.__forceLocal:
            self.__forceUpdate = False
        self.main()
        sys.exit(0)

    def exit_gracefully(self, signum, frame):
        signal.signal(signal.SIGINT, self.original_sigint)
        if float(sys.version[:3]) < 3.0:
            real_raw_input = raw_input
        else:
            real_raw_input = input
        try:
            if real_raw_input(b'\nReally quit? (y/n)> ').lower().startswith(b'y'):
                sys.exit(1)
        except KeyboardInterrupt:
            print b'Ok ok, quitting'
            sys.exit(1)

        signal.signal(signal.SIGINT, self.exit_gracefully)


Base = declarative_base()

class TVShow(Base):
    __tablename__ = b'THETVDB'
    id = Column(Integer, primary_key=True, autoincrement=b'ignore_fk')
    seriesid = Column(Integer)
    season = Column(Integer)
    totalnumofepisodes = Column(Integer)
    lastupdated = Column(REAL)


if __name__ == b'__main__':
    sms = TVShows()
    sms.getArguments(sys.argv[1:])