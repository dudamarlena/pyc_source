# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/watcher.py
# Compiled at: 2014-10-17 03:59:41
import sys, json, logging, hashlib, urllib2, urllib
from sys import exit
from zlib import compress
from config import titanConfig
from binascii import b2a_hex, hexlify
from os import path, walk, remove, environ
from titan import __version__ as version, http
from titan.tools.orm import TiORM as titanORM
from time import sleep, strftime, strptime, gmtime, mktime
from titan.tools.system import shell_out, hw_serial as get_device_serial
from os.path import dirname, realpath, isfile, join, splitext, basename
TITAN_PATH = environ.get('TITAN_PATH') or '/var/lib/titan/'
TITAN_CONFIG = join('/etc/', 'titan.conf')
CONFIG = titanConfig(TITAN_CONFIG, TITAN_PATH)
DATASTORE = CONFIG['main']['datastore']
ORM = titanORM(DATASTORE)
DEVICEID = get_device_serial()
RUN_PREFIX = '[%s] ' % strftime('%a, %d %b %Y %H:%M:%S-%Z', gmtime())
TOKEN = {'token': CONFIG['reporting']['token']}
ORM.initialize_table('watcher', {'date': {'nullable': False, 'type': 'text'}, 'utime': {'type': 'integer'}, 'module': {'type': 'text'}, 'status': {'type': 'integer'}})
if CONFIG['reporting']['target'] is None or CONFIG['reporting']['target'] == '':
    print '[!] No place to report to'
    exit()
REPORTING_TARGET = '%s%s%s' % (CONFIG['reporting']['target'], 'api/observer/', DEVICEID)
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
        last_success = ORM.raw_sql('SELECT * FROM watcher WHERE module="%s" AND status=1 ORDER BY date DESC LIMIT 1' % table['name'])
        if len(last_success) is 0:
            temp_utime = unix_time
            ORM.raw_sql("INSERT INTO watcher (date,status,utime,module) VALUES ('%s', 0,'%s', '%s')" % (exec_time, temp_utime, table['name']))
            logging.info('%sCollecting data for [%s] since ever' % (RUN_PREFIX, table['name']))
            results = ORM.select(table['name'], '*')
        else:
            temp_utime = int(last_success[0][4])
            logging.info('%sCollecting data for [%s] since %s' % (RUN_PREFIX, table['name'], last_success[0][1]))
            results = ORM.select(table['name'], '*', 'unixtime > %d' % temp_utime)
        if results is None:
            ORM.raw_sql("UPDATE watcher SET status=0, utime = '%d' WHERE module = '%s'" % (unix_time, table['name']))
            continue
        else:
            if len(results) > 0:
                pass
            else:
                ORM.raw_sql("UPDATE watcher SET status=0, utime = '%d' WHERE module = '%s'" % (unix_time, table['name']))
                continue
            table_json = json.dumps({'module': table['name'], 'data': results})
            compressed = compress(table_json)
            content_digest = hashlib.sha256(compressed).hexdigest()
            logging.info("\tSending request to '%s'" % REPORTING_TARGET)
            code, response = http.request(REPORTING_TARGET, {'serial': DEVICEID, 'digest': content_digest, 'stream': compressed})
            try:
                logging.info("\tResponse: [%d] @ '%s'" % (code, response))
            except:
                logging.info("\tResponse: [%d] @ '%s'" % (code, response))

        if code == 202:
            passes_had += 1
            ORM.raw_sql("UPDATE watcher SET status=1, utime = %d WHERE module = '%s'" % (unix_time, table['name']))
        else:
            ORM.raw_sql("UPDATE watcher SET status=0, utime = %d WHERE module = '%s'" % (temp_utime, table['name']))

    exit()
    return


def test_waters(target):
    try:
        request = urllib2.Request(target)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'titanOSX %s' % version),
         (
          'X-Titan-Token', CONFIG['reporting']['token'])]
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
    code = 0
    while True:
        code, res = test_waters(REPORTING_TARGET)
        if code == 203:
            logging.info('%sWatcher detected a connection ' % RUN_PREFIX)
            generate_reports()
        elif code == 404:
            logging.info('%sPlease register this device first ' % RUN_PREFIX)
            exit()
        else:
            seconds = 2 ** try_count
            if seconds >= 2047:
                exit()
            try_count += 1
            logging.info('%sWatcher did not detect a connection, retrying in %d seconds' % (RUN_PREFIX, seconds))
            sleep(seconds)


if __name__ == '__main__':
    run()