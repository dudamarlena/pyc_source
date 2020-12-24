# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/watcher.py
# Compiled at: 2014-08-24 10:35:20
import sys, logging, hashlib
from ctznosx import __version__ as version
from sys import exit
import urllib2, urllib, httplib, json
from os import path, walk, remove, environ
from os.path import dirname, realpath, isfile, join, splitext, basename
from binascii import b2a_hex, hexlify
from config import ctznConfig
from titantools.orm import TiORM as ctznORM
from titantools.system import shell_out, hw_serial as get_device_serial
from zlib import compress
from time import sleep, strftime, strptime, gmtime, mktime
CTZNOSX_PATH = environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/'
CTZNOSX_CONFIG = join('/etc/', 'ctznosx.conf')
CONFIG = ctznConfig(CTZNOSX_CONFIG, CTZNOSX_PATH)
DATASTORE = CONFIG['main']['datastore']
ORM = ctznORM(DATASTORE)
DEVICEID = get_device_serial()
RUN_PREFIX = '[%s] ' % strftime('%a, %d %b %Y %H:%M:%S-%Z', gmtime())
ORM.initialize_table('watcher', {'date': {'nullable': False, 'type': 'text'}, 'utime': {'type': 'integer'}, 'module': {'type': 'text'}, 'status': {'type': 'integer'}})
REPORTING_TARGET = '%s%s' % (CONFIG['reporting']['target'], 'observer')
if REPORTING_TARGET is None or REPORTING_TARGET == '':
    print '[!] No place to report to'
    exit()
if CONFIG['watcher']['enabled'] is 'false':
    print '[!] Watcher is disabled'
    exit()
logging.basicConfig(format='%(message)s', level=logging.INFO)

def generate_reports():
    unix_time = int(mktime(gmtime()))
    exec_time = strftime('%a, %d %b %Y %H:%M:%S-%Z', gmtime())
    all_tables = ORM.select('sqlite_master', 'name', "type = 'table' and name != 'watcher'")
    passes_needed = 0
    passes_had = 0
    for table in [ table for table in all_tables ]:
        last_success = ORM.raw_sql('SELECT * FROM watcher WHERE module="%s" ORDER BY date DESC LIMIT 1' % table['name'])
        if len(last_success[0]) is 0:
            temp_utime = unix_time
            ORM.raw_sql("INSERT INTO watcher (date,status,utime,module) VALUES ('%s', 0,'%s', '%s')" % (exec_time, temp_utime, table['name']))
            logging.info('%sCollecting data for [%s] since ever' % (RUN_PREFIX, table['name']))
            results = ORM.select(table['name'], '*')
        else:
            temp_utime = int(last_success[0][4])
            logging.info('%sCollecting data for [%s] since %s' % (RUN_PREFIX, table['name'], last_success[0][1]))
            results = ORM.select(table['name'], '*', 'unixtime > %d' % temp_utime)
        if results is None or len(results) == 0:
            ORM.raw_sql("UPDATE watcher SET status=0, utime = '%d' WHERE module = '%s'" % (unix_time, table['name']))
            continue
        table_json = json.dumps({'module': table['name'], 'data': results})
        compressed = compress(table_json)
        content_digest = hashlib.sha256(compressed).hexdigest()
        target = '%s/%s' % (REPORTING_TARGET, DEVICEID)
        logging.info("\tSending request to '%s'" % target)
        code, response = send_request(target, {'serial': DEVICEID, 'digest': content_digest, 'stream': compressed})
        try:
            logging.info("\tResponse: [%d] @ '%s'" % (code, response.read()))
        except:
            logging.info("\tResponse: [%d] @ '%s'" % (code, response))

        if code == 202:
            passes_had += 1
            ORM.raw_sql("UPDATE watcher SET status=1, utime = %d WHERE module = '%s'" % (unix_time, table['name']))
        else:
            ORM.raw_sql("UPDATE watcher SET status=0, utime = %d WHERE module = '%s'" % (temp_utime, table['name']))

    exit()
    return


def send_request(target, data):
    try:
        request = urllib2.Request(target, urllib.urlencode(data))
        request.add_header('User-Agent', 'ctznOSX %s' % version)
        opener = urllib2.build_opener()
        response = opener.open(request)
        response_object = (response.getcode(), response)
    except urllib2.HTTPError as e:
        response_object = (
         e.code, e.read())
    except urllib2.URLError as e:
        response_object = (0, 'Connection Refused')

    return response_object


def run():
    try_count = 0
    while True:
        try:
            target = '%s/%s' % (REPORTING_TARGET, DEVICEID)
            logging.info("%sChecking connectivity to: '%s'" % (RUN_PREFIX, target))
            code, response = send_request(target, {'serial': DEVICEID, 'ping': 'ping'})
        except:
            pass

        if code == 203:
            logging.info('%sWatcher detected a connection ' % RUN_PREFIX)
            generate_reports()
        else:
            seconds = 3 ** try_count
            if seconds >= 3600:
                exit()
            try_count += 1
            logging.info('%sWatcher did not detect a connection, retrying in %d seconds' % (RUN_PREFIX, seconds))
            sleep(seconds)


if __name__ == '__main__':
    run()