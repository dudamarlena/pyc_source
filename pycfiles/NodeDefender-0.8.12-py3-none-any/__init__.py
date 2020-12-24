# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/config/__init__.py
# Compiled at: 2018-03-09 03:40:48
import NodeDefender, NodeDefender.config.celery, NodeDefender.config.database, NodeDefender.config.general, NodeDefender.config.logging, NodeDefender.config.mail, NodeDefender.config.redis, configparser, os
deployed = False
configfile = None
parser = configparser.ConfigParser()
basepath = os.path.abspath(os.path.dirname('..'))
datafolder = None
if os.path.exists(basepath + '/manage.py'):
    datafolder = basepath
else:
    datafolder = os.path.expanduser('~') + '/.nodedefender'
    if not os.path.isdir(datafolder):
        print ('Creating folder: {}').format(datafolder)
        os.makedirs(datafolder)
configfile = datafolder + '/NodeDefender.conf'
migrations_folder = datafolder + '/sql_migrations'

def write_default():
    NodeDefender.config.celery.set_default()
    NodeDefender.config.database.set_default()
    NodeDefender.config.general.set_default()
    NodeDefender.config.logging.set_default()
    NodeDefender.config.mail.set_default()
    NodeDefender.config.redis.set_default()
    return write()


def load(fname=None):
    global deployed
    if os.path.exists(configfile):
        parser.read(configfile)
    else:
        return False
    if not eval(parser['DATABASE']['ENABLED']):
        return False
    deployed = True
    NodeDefender.config.celery.load_config(parser)
    NodeDefender.config.database.load_config(parser)
    NodeDefender.config.general.load_config(parser)
    NodeDefender.config.logging.load_config(parser)
    NodeDefender.config.mail.load_config(parser)
    NodeDefender.config.redis.load_config(parser)
    return True


def write():
    with open(configfile, 'w') as (fw):
        parser.write(fw)