# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/loggers/csv.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 578 bytes
import os, configparser

def log(source, function, duration, success, configpath):
    logurl = 'snafu.csv'
    if not configpath:
        configpath = 'snafu.ini'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if 'snafu' in config and 'logger.csv' in config['snafu']:
            logurl = config['snafu']['logger.csv']
    f = open(logurl, 'a')
    print('{},{},{:1.3f},{}'.format(source, function, duration, success), file=f)
    f.close()