# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seshet/config.py
# Compiled at: 2015-07-16 08:31:30
# Size of source mod 2**32: 3806 bytes
"""Define default configuration, read configuration file, and apply
configuration to SeshetBot instance.
"""
from configparser import ConfigParser
from pydal import DAL, Field
default_config = '\n[connection]\n# passed to SeshetBot.connect()\nserver: chat.freenode.net\nport: 6667\nchannels: #botwar\nssl: False\n\n[client]\nnickname: Seshet\nuser: seshet\nrealname: seshetbot\n\n[welcome]\n# stuff sent by the bot after connecting\nuse_nickserv: False\nnickserv_pass:\nuser_mode: -x\n\n[locale]\ntimezone: UTC\nlocale: en_US\n# see docs for datetime.strftime\ndate_fmt: %m%d%y\n# 071415\ntime_fmt: %H:%M:%S\n# 11:49:57\nshort_datetime_fmt: %Y-%m-%d %H:%M:%S\n# 2015-07-14 11:49:57\nlong_datetime_fmt: %A %d %B %Y at %H:%M:%S %Z\n# Tuesday 14 July 2015 at 11:49:57 UTC\n\n[database]\nuse_db: True\ndb_string: sqlite://seshet.db\n\n[logging]\n# if using db, this will be ignored\nfile: logs/%(target)s_%(date)s.log\n\n[debug]\n# corresponds to levels in logging module or None\nverbosity: warning\nfile: seshet-debug.log\n'
testing_config = '\n[connection]\n# passed to SeshetBot.connect()\nserver: chat.freenode.net\nport: 6667\nchannels: #botwar\nssl: False\n\n[client]\nnickname: Seshet\nuser: seshet\nrealname: seshetbot\n\n[welcome]\n# stuff sent by the bot after connecting\nuse_nickserv: False\nnickserv_pass:\nuser_mode: -x\n\n[locale]\ntimezone: UTC\nlocale: en_US\n# see docs for datetime.strftime\ndate_fmt: %m%d%y\n# 071415\ntime_fmt: %H:%M:%S\n# 11:49:57\nshort_datetime_fmt: %Y-%m-%d %H:%M:%S\n# 2015-07-14 11:49:57\nlong_datetime_fmt: %A %d %B %Y at %H:%M:%S %Z\n# Tuesday 14 July 2015 at 11:49:57 UTC\n\n[database]\n# no db connection for testing\nuse_db: False\n\n[logging]\n# if using db, this will be ignored\nfile: logs/%(target)s_%(date)s.log\n\n[debug]\n# corresponds to levels in logging module or None\nverbosity: debug\nfile: seshet-debug.log\n'

def build_db_tables(db):
    """Build Seshet's basic database schema. Requires one parameter,
    `db` as `pydal.DAL` instance.
    """
    if not isinstance(db, DAL) or not db._uri:
        raise Exception('Need valid DAL object to define tables')
    db.define_table('event_log', Field('event_type'), Field('event_time', 'datetime'), Field('source'), Field('target'), Field('message', 'text'), Field('host'), Field('parms', 'list:string'))


def build_bot(config_file=None):
    """Parse a config and return a SeshetBot instance. After, the bot can be run
    simply by calling .connect() and then .start()
    
    Optional arguments:
        config_file - valid file path or ConfigParser instance
        
        If config_file is None, will read default config defined in this module.
    """
    from . import bot
    config = ConfigParser()
    if config_file is None:
        config.read_string(default_config)
    else:
        if isinstance(config_file, ConfigParser):
            config = config_file
        else:
            config.read(config_file)
        db_conf = config['database']
        conn_conf = config['connection']
        client_conf = config['client']
        if db_conf.getboolean('use_db'):
            db = DAL(db_conf['db_string'])
            build_db_tables(db)
        else:
            db = None
    seshetbot = bot.SeshetBot(client_conf['nickname'], db)
    seshetbot.default_host = conn_conf['server']
    seshetbot.default_port = int(conn_conf['port'])
    seshetbot.default_channel = conn_conf['channels'].split(',')
    seshetbot.default_use_ssl = conn_conf.getboolean('ssl')
    seshetbot.user = client_conf['user']
    seshetbot.real_name = client_conf['realname']
    return seshetbot