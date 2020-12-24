# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\maha_cet_parser\commands\CreateTableMySQL.py
# Compiled at: 2020-04-12 16:02:46
# Size of source mod 2**32: 8902 bytes
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Integer, Table, Column, text, String, ForeignKey, Boolean, Float, Enum, TEXT
from maha_cet_parser.admission_enums import SeatType, Gender
from .Commands import Command
import tempfile, logging, os, calendar, time

def get_metadat():
    metadata = MetaData()
    universityTable = Table('university', metadata, Column('id', Integer, primary_key=True, autoincrement=True), Column('code', String(length=400), unique=True), Column('name', TEXT, nullable=False), Column('city', String(length=400)))
    collageTable = Table('collage', metadata, Column('id', Integer, primary_key=True, autoincrement=True), Column('code', String(length=400), unique=True), Column('name', String(length=400)), Column('isAided', (Boolean()), default=False), Column('home_university', Integer, (ForeignKey('university.id')), default='NULL'), Column('city', String(length=400)))
    branchTable = Table('branch', metadata, Column('id', Integer, primary_key=True, autoincrement=True), Column('collage_code', Integer, (ForeignKey('collage.id')), default='NULL'), Column('code', String(length=400), nullable=False, unique=True), Column('name', String(length=400)))
    admissioncutoffTable = Table('admissioncutoff', metadata, Column('id', Integer, primary_key=True, autoincrement=True), Column('seat_type', Enum(SeatType)), Column('rank', Integer, nullable=False), Column('percentile', Float, nullable=False), Column('branch_code', Integer, (ForeignKey('branch.id')), nullable=False), Column('admission_year', (String(16)), nullable=False), Column('level', Integer, nullable=False), Column('stage', Integer, nullable=False), Column('round', Integer, nullable=False))
    studentTable = Table('student', metadata, Column('id', Integer, primary_key=True), Column('rank', Integer, nullable=False), Column('mhcet_score', Float, nullable=False), Column('mhcet_application_id', (String(20)), nullable=False, unique=True), Column('candidate_name', (String(40)), nullable=False), Column('gender', Enum(Gender)), Column('candidate_category', (String(40)), nullable=False), Column('seat_type', Enum(SeatType)))
    return metadata


class CreateTableMySQL(Command):

    def __init__(self, args):
        """Intialize the object by using the arguments from argparse"""
        Command.__init__(self, args)
        self.load_arg_or_default(args, 'db_dialect')
        self.load_arg_or_default(args, 'db_driver')
        self.load_arg_or_default(args, 'db_username')
        self.load_arg_or_default(args, 'db_password')
        self.load_arg_or_default(args, 'db_hostname')
        self.load_arg_or_default(args, 'db_port')
        self.load_arg_or_default(args, 'db_name')
        self.ts = calendar.timegm(time.gmtime())
        self.logger = logging.getLogger(__name__)
        self.logsDir = os.path.join(tempfile.gettempdir(), 'maha_cet_admission', 'logs')
        if not os.path.exists(self.logsDir):
            os.makedirs(self.logsDir)
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    @staticmethod
    def add_args(subparsers):
        parser = subparsers.add_parser('eng_admission')
        subparsers2 = parser.add_subparsers(help='Argument for Engineering admission')
        populatedb_parser = subparsers2.add_parser('create_db_tables')
        populatedb_parser.add_argument('-d', '--db_dialect', help='Database dialect Name', env_var='DATABASE_DIALECT_NAME',
          default='mysql')
        populatedb_parser.add_argument('-dd', '--db_driver', help='Database driver', env_var='DATABASE_DRIVER_NAME', default='pymysql')
        populatedb_parser.add_argument('-u', '--db_username', help='Database user name', env_var='DATABASE_USER_NAME', default='root')
        populatedb_parser.add_argument('-p', '--db_password', help='Database user password', env_var='DATABASE_USER_PASSWORD',
          default='root')
        populatedb_parser.add_argument('-host', '--db_hostname', help='Database host name', env_var='DATABASE_HOSTNAME', default='localhost')
        populatedb_parser.add_argument('-dp', '--db_port', help='Database port', env_var='DATABASE_PORT', default='3306')
        populatedb_parser.add_argument('-n', '--db_name', help='Database connection name', env_var='DB_SID_NAME', default='admissiondb')
        populatedb_parser.set_defaults(func=(CreateTableMySQL.create_db_tables))

    def get_engine_url(self):
        engine_url = self.db_dialect + '+' + self.db_driver + '://' + self.db_username + ':' + self.db_password + '@' + self.db_hostname + ':' + self.db_port + '/' + self.db_name
        self.logger.info('Database Engine url is')
        self.logger.info(engine_url)
        return engine_url

    def get_engine(self):
        engine_url = self.get_engine_url()
        engine = create_engine(engine_url)
        return engine

    def run_create_db_tables(self):
        logfileName = 'create_db_tables_' + str(self.ts) + '.log'
        log_file_name = os.path.join(self.logsDir, logfileName)
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=(logging.INFO),
          handlers=[
         logging.FileHandler(log_file_name, mode='w', encoding=None, delay=False),
         logging.StreamHandler()])
        engine = self.get_engine()
        metadata = get_metadat()
        metadata.create_all(engine)
        self.logger.info(tempfile.gettempdir())
        self.logger.info('Succesfully created database following tables')
        self.logger.info(engine.table_names())

    @staticmethod
    def create_db_tables(args):
        utils = CreateTableMySQL(args)
        utils.run_create_db_tables()