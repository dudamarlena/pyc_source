# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/loggers/sqlite.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 811 bytes
import sqlite3, os, configparser

def log(source, function, duration, success, configpath):
    logurl = '/tmp/snafu.sqlite'
    if not configpath:
        configpath = 'snafu.ini'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if 'snafu' in config and 'logger.sqlite' in config['snafu']:
            logurl = config['snafu']['logger.sqlite']
    init = False
    if not os.path.isfile(logurl):
        init = True
    conn = sqlite3.connect(logurl)
    c = conn.cursor()
    if init:
        c.execute('CREATE TABLE log (source text, function text, duration real, success bool)')
    c.execute("INSERT INTO log (source, function, duration, success) VALUES ('{}', '{}', {}, '{}')".format(source, function, duration, success))
    conn.commit()
    conn.close()