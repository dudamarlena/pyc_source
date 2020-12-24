# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ecommstackstatus/ecommStackStatus.py
# Compiled at: 2016-06-02 16:49:34
"""
Magento is a trademark of Varien. Neither I nor these scripts are affiliated with or endorsed by the Magento Project or its trademark owners.

"""
STACK_STATUS_VERSION = 2016051601
error_collection = []
from ecommstacklib import *
import re, glob, subprocess, sys, os, fnmatch
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET

import pprint, socket, collections
try:
    import json
    JSON = True
except ImportError:
    JSON = False

try:
    import argparse
    ARGPARSE = True
except ImportError:
    ARGPARSE = False
    sys.stderr.write('This program is more robust if python argparse installed.\n')

try:
    import mysql.connector
    MYSQL = True
except ImportError:
    MYSQL = False

class argsAlt(object):
    pass


pp = pprint.PrettyPrinter(indent=4)
if ARGPARSE:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-j', '--jsonfile', help='Name of a config dump json file. Skips detection and uses file values.')
    parser.add_argument('-s', '--silent', help='No output, not even stderr.', action='store_true')
    parser.add_argument('-v', '--verbose', help='Additional output, mostly to stderr.', action='store_true')
    parser.add_argument('-F', '--nofiglet', help='Omits big text (figlet) banners. Banners do not require figlet to be installed.', action='store_true')
    parser.add_argument('-f', '--force', help='If config_dump.json already exists, overwrite it. Default: do not overwrite.', action='store_true')
    parser.add_argument('-o', '--output', help='Name of json file to place saved config in. Default: ./config_dump.json', default='./config_dump.json')
    parser.add_argument('--printwholeconfig', help='Print the concat (whole) config of a daemon(s). Requires additional daemon switches.', action='store_true')
    parser.add_argument('--apache', help='Daemon specific switch for other options (printwholeconfig)', action='store_true')
    parser.add_argument('--nginx', help='Daemon specific switch for other options (printwholeconfig)', action='store_true')
    parser.add_argument('--phpfpm', help='Daemon specific switch for other options (printwholeconfig)', action='store_true')
    parser.add_argument('--printglobalconfig', help='Pretty print the globalconfig dict', action='store_true')
    parser.add_argument('--printjson', help='Pretty print the globalconfig json', action='store_true')
    parser.add_argument('--nomagento', help='Skip Magento detection; it will detect apache, nginx and php-fpm for normal L?MP stacks', action='store_true')
    args = parser.parse_args()
else:
    args = argsAlt()
    args.jsonfile = None
    args.silent = None
    args.verbose = None
    args.nofiglet = None
    args.force = None
    args.printwholeconfig = None
    args.printglobalconfig = None
    args.apache = None
    args.nginx = None
    args.phpfpm = None
    args.output = './config_dump.json'
    args.printjson = None
    args.nomagento = None
if args.jsonfile and JSON == True:
    if os.path.isfile(args.jsonfile):
        if True:
            f = open(args.jsonfile, 'r')
            globalconfig = json.load(f)
    else:
        sys.stderr.write('The file %s does not exist.\n' % args.jsonfile)
        error_collection.append('The file %s does not exist.\n' % args.jsonfile)
        sys.exit(1)
apache = apacheCtl()
nginx = nginxCtl()
phpfpm = phpfpmCtl()
magento = MagentoCtl()
redis = RedisCtl()
memcache = MemcacheCtl()
if not args.jsonfile:
    daemons = daemon_exe(['httpd', 'apache2', 'nginx', 'bash', 'httpd.event', 'httpd.worker', 'php-fpm', 'mysql', 'mysqld'])
    for i in daemons:
        if daemons.get(i, {}).get('error'):
            sys.stderr.write(daemons[i]['error'] + '\n')
            error_collection.append(daemons[i]['error'] + '\n')

    localfqdn = socket.getfqdn()
    globalconfig = {'version': STACK_STATUS_VERSION, 'fqdn': localfqdn}
    globalconfig['daemons'] = daemons

    class DATA_GATHER(object):
        pass


    def APACHE_DATA_GATHER():
        pass


    sys.stderr.write('apache data gather\n')
    apache_exe = ''
    if 'apache2' in daemons:
        apache_basename = daemons['apache2']['basename']
        apache_exe = daemons['apache2']['exe']
        apache = apacheCtl(exe=daemons['apache2']['exe'])
    elif 'httpd' in daemons:
        apache_basename = daemons['httpd']['basename']
        apache_exe = daemons['httpd']['exe']
        apache = apacheCtl(exe=daemons['httpd']['exe'])
    elif 'httpd.event' in daemons:
        apache_basename = daemons['httpd.event']['basename']
        apache_exe = daemons['httpd.event']['exe']
        apache = apacheCtl(exe=daemons['httpd.event']['exe'])
    elif 'httpd.worker' in daemons:
        apache_basename = daemons['httpd.worker']['basename']
        apache_exe = daemons['httpd.worker']['exe']
        apache = apacheCtl(exe=daemons['httpd.worker']['exe'])
    else:
        sys.stderr.write('Apache is not running\n')
        error_collection.append('Apache is not running\n')
    if apache_exe:
        if True:
            apache_conf_file = apache.get_conf()
            apache_root_path = apache.get_root()
            apache_mpm = apache.get_mpm()
        if apache_conf_file and apache_root_path:
            sys.stderr.write('Using config %s\n' % apache_conf_file)
            error_collection.append('Using config %s\n' % apache_conf_file)
            wholeconfig = importfile(apache_conf_file, '\\s*include(?:optional?)?\\s+[\'"]?([^\\s\'"]+)[\'"]?', base_path=apache_root_path)
            if args.printwholeconfig and args.apache:
                print wholeconfig
            apache_config = apache.parse_config(wholeconfig)
            if 'apache' not in globalconfig:
                globalconfig['apache'] = {}
            globalconfig['apache'] = apache_config
            globalconfig['apache']['version'] = apache.get_version()
            daemon_config = apache.get_conf_parameters()
            if daemon_config:
                if 'daemon' not in globalconfig['apache']:
                    globalconfig['apache']['daemon'] = daemon_config
                globalconfig['apache']['basename'] = apache_basename
                globalconfig['apache']['exe'] = daemons[apache_basename]['exe']
                globalconfig['apache']['cmd'] = daemons[apache_basename]['cmd']

    def NGINX_DATA_GATHER():
        pass


    sys.stderr.write('nginx data gather\n')
    if 'nginx' not in daemons:
        sys.stderr.write('nginx is not running\n')
        error_collection.append('nginx is not running\n')
    else:
        nginx = nginxCtl(exe=daemons['nginx']['exe'])
        if True:
            nginx_conf_file = nginx.get_conf()
        if nginx_conf_file:
            sys.stderr.write('Using config %s\n' % nginx_conf_file)
            error_collection.append('Using config %s\n' % nginx_conf_file)
            wholeconfig = importfile(nginx_conf_file, '\\s*include\\s+(\\S+);')
            if args.printwholeconfig and args.nginx:
                print wholeconfig
            nginx_config = nginx.parse_config(wholeconfig)
            if 'nginx' not in globalconfig:
                globalconfig['nginx'] = {}
            globalconfig['nginx'] = nginx_config
            globalconfig['nginx']['version'] = nginx.get_version()
            daemon_config = nginx.get_conf_parameters()
            if daemon_config:
                if 'daemon' not in globalconfig['nginx']:
                    globalconfig['nginx']['daemon'] = daemon_config
                globalconfig['nginx']['basename'] = 'nginx'
                globalconfig['nginx']['exe'] = daemons['nginx']['exe']
                globalconfig['nginx']['cmd'] = daemons['nginx']['cmd']

    def PHP_FPM_DATA_GATHER():
        pass


    sys.stderr.write('php-fpm data gather\n')
    if 'php-fpm' not in daemons:
        sys.stderr.write('php-fpm is not running\n')
        error_collection.append('php-fpm is not running\n')
    else:
        phpfpm = phpfpmCtl(exe=daemons['php-fpm']['exe'])
        if True:
            phpfpm_conf_file = phpfpm.get_conf()
        if phpfpm_conf_file:
            wholeconfig = importfile(phpfpm_conf_file, '\\s*include[\\s=]+(\\S+)')
            if args.printwholeconfig and args.phpfpm:
                print wholeconfig
            phpfpm_config = phpfpm.parse_config(wholeconfig)
            if 'php-fpm' not in globalconfig:
                globalconfig['php-fpm'] = {}
            globalconfig['php-fpm'] = phpfpm_config
            globalconfig['php-fpm']['version'] = phpfpm.get_version()
            globalconfig['php-fpm']['basename'] = 'php-fpm'
            globalconfig['php-fpm']['exe'] = daemons['php-fpm']['exe']
            globalconfig['php-fpm']['cmd'] = daemons['php-fpm']['cmd']
    if not args.nomagento:

        def MAGENTO_DATA_GATHER():
            pass


        sys.stderr.write('magento data gather\n')
        doc_roots = set()
        if globalconfig.get('apache', {}).get('sites'):
            for one in globalconfig['apache']['sites']:
                if 'doc_root' in one:
                    doc_roots.add(one['doc_root'])

        if globalconfig.get('nginx', {}).get('sites'):
            for one in globalconfig['nginx']['sites']:
                if 'doc_root' in one:
                    doc_roots.add(one['doc_root'])

        globalconfig['doc_roots'] = list(doc_roots)
        if 'magento' not in globalconfig:
            globalconfig['magento'] = {}
        if True:
            mage_files = magento.find_mage_php(globalconfig['doc_roots'])
        mage_file_info = magento.mage_file_info(mage_files)
        globalconfig['magento']['doc_root'] = mage_file_info
        mage_file_info = magento.mage_file_info(mage_files)
        globalconfig['magento']['doc_root'] = mage_file_info
        for doc_root in globalconfig['magento']['doc_root']:
            if doc_root not in globalconfig['magento']['doc_root']:
                globalconfig['magento']['doc_root'][doc_root] = {}
            local_xml = globalconfig['magento']['doc_root'][doc_root]['local_xml']['filename']
            if 'local_xml' not in globalconfig['magento']['doc_root'][doc_root]:
                globalconfig['magento']['doc_root'][doc_root]['local_xml'] = {}
            update(globalconfig['magento']['doc_root'][doc_root]['local_xml'], magento.open_local_xml(doc_root, globalconfig['magento']['doc_root'][doc_root]))
            update(globalconfig['magento']['doc_root'][doc_root], magento.db_cache_table(doc_root, globalconfig['magento']['doc_root'][doc_root].get('local_xml', {}).get('db', {})))

        def MEMCACHE_DATA_GATHER():
            pass


        sys.stderr.write('memcache data gather\n')
        memcache_instances = memcache.instances(globalconfig.get('magento', {}).get('doc_root', {}))
        if not globalconfig.get('memcache') and memcache_instances:
            globalconfig['memcache'] = {}
        if memcache_instances:
            update(globalconfig['memcache'], memcache.get_all_statuses(memcache_instances))

        def REDIS_DATA_GATHER():
            pass


        sys.stderr.write('redis data gather\n')
        redis_instances = redis.instances(globalconfig.get('magento', {}).get('doc_root', {}))
        if not globalconfig.get('redis') and redis_instances:
            globalconfig['redis'] = {}
        if redis_instances:
            update(globalconfig['redis'], redis.get_all_statuses(redis_instances))

    def MYSQL_DATA_GATHER():
        pass


    sys.stderr.write('mysql data gather\n')
    if 'mysql' not in globalconfig:
        globalconfig['mysql'] = {}
else:
    for i in globalconfig['errors']:
        sys.stdout.write(i)

class OUTPUT(object):
    pass


print 'FQDN: %s' % localfqdn

def NGINX_PRINT():
    pass


if 'nginx' in globalconfig:
    nginx.figlet()
    if globalconfig.get('nginx', {}).get('version'):
        print globalconfig.get('nginx', {}).get('version')
    else:
        print 'No nginx version?'
    if globalconfig.get('nginx', {}).get('sites'):
        print 'nginx sites:'
        if globalconfig.get('nginx', {}).get('error'):
            sys.stderr.write('Errors: \n%s\n' % globalconfig['nginx']['error'])
            error_collection.append('Errors: \n%s\n' % globalconfig['nginx']['error'])
        print_sites(globalconfig['nginx']['sites'])
        if globalconfig.get('nginx', {}).get('basename') and globalconfig.get('nginx', {}).get('maxprocesses'):
            proc_name = globalconfig['nginx']['basename']
            proc_max = int(globalconfig['nginx']['maxprocesses'])
            result = memory_estimate(proc_name)
            if result:
                memory_print(result, proc_name, proc_max)
        print

def APACHE_PRINT():
    pass


if 'apache' in globalconfig:
    apache.figlet()
    if globalconfig.get('apache', {}).get('version'):
        print 'Apache version: %s' % globalconfig.get('apache', {}).get('version')
    else:
        print 'No apache version?'
    if globalconfig.get('apache', {}).get('daemon', {}).get('Server MPM'):
        print 'Apache server MPM: %s\n' % globalconfig.get('apache', {}).get('daemon', {}).get('Server MPM')
    else:
        print 'No apache server MPM?\n'
    if globalconfig.get('apache', {}).get('sites'):
        print 'Apache sites:'
        print_sites(globalconfig['apache']['sites'])
        if 'basename' in globalconfig['apache'] and 'maxprocesses' in globalconfig['apache']:
            proc_name = globalconfig['apache']['basename']
            proc_max = globalconfig['apache']['maxprocesses']
            result = memory_estimate(proc_name)
            if result:
                memory_print(result, proc_name, proc_max)
        print '\n'

def PHP_FPM_PRINT():
    pass


if 'php-fpm' in globalconfig:
    phpfpm.figlet()
    if globalconfig.get('php-fpm', {}).get('version'):
        print 'php-fpm version: %s' % globalconfig.get('php-fpm', {}).get('version')
    else:
        print 'No php version?'
    print 'php-fpm pools:'
    for one in globalconfig['php-fpm']:
        if type(globalconfig['php-fpm'][one]) is dict:
            print '%s' % (one,)

    print
    print 'php-fpm memory profile:'
    if globalconfig.get('php-fpm', {}).get('basename') and globalconfig.get('php-fpm', {}).get('maxprocesses'):
        proc_name = globalconfig['php-fpm']['basename']
        proc_max = int(globalconfig['php-fpm']['maxprocesses'])
        result = memory_estimate(proc_name)
        if result:
            memory_print(result, proc_name, proc_max)

def MAGENTO_PRINT():
    pass


if globalconfig.get('magento', {}).get('doc_root'):
    magento.figlet()
    print '\nMagento versions installed:'
    if globalconfig.get('magento', {}).get('doc_root'):
        for key, value in globalconfig['magento']['doc_root'].iteritems():
            print '-' * 60
            print 'Magento path: %s' % key
            print 'local.xml: %s' % value['local_xml']['filename']
            print 'Version: %s' % value['magento_version']
            print
            skip = [
             'pdoType', 'initStatements', 'model', 'type']
            if value.get('local_xml', {}).get('db'):
                print 'Database info'
                for k2, v2 in value['local_xml']['db'].iteritems():
                    if k2 in skip:
                        continue
                    print '%s: %s' % (k2, v2)

                print
            skip = [
             'engine', 'disable_locking', 'compression_threshold',
             'log_level', 'first_lifetime', 'bot_first_lifetime',
             'bot_lifetime', 'compression_lib', 'break_after_adminhtml',
             'break_after_frontend', 'connect_retries']
            if value.get('local_xml', {}).get('session_cache', {}).get('session_save'):
                print 'Session Cache engine: %s' % value.get('local_xml', {}).get('session_cache', {}).get('engine', 'EMPTY')
                print 'Session Cache: %s' % value['local_xml']['session_cache']['session_save']
                for k2, v2 in value['local_xml']['session_cache'].iteritems():
                    if k2 in skip:
                        continue
                    print '%s: %s' % (k2, v2)

                print
            skip = [
             'engine', 'compress_tags', 'use_lua',
             'automatic_cleaning_factor', 'force_standalone',
             'compress_data', 'compress_threshold',
             'compression_lib', 'connect_retries']
            if value.get('local_xml', {}).get('object_cache', {}).get('backend'):
                print 'Object Cache engine: %s' % value.get('local_xml', {}).get('object_cache', {}).get('engine', 'EMPTY')
                print 'Object Cache: %s' % value.get('local_xml', {}).get('object_cache', {}).get('backend', 'EMPTY')
                for k2, v2 in value['local_xml']['object_cache'].iteritems():
                    if k2 in skip:
                        continue
                    print '%s: %s' % (k2, v2)

                print
            skip = [
             'engine', 'connect_retries', 'force_standalone',
             'compress_data']
            if value.get('local_xml', {}).get('full_page_cache', {}).get('backend'):
                print 'Full Page Cache engine: %s' % value.get('local_xml', {}).get('full_page_cache', {}).get('engine', 'EMPTY')
                print 'Full Page Cache: %s' % value.get('local_xml', {}).get('full_page_cache', {}).get('backend', 'EMPTY')
                for k2, v2 in value['local_xml']['full_page_cache'].iteritems():
                    if k2 in skip:
                        continue
                    print '%s: %s' % (k2, v2)

                print
            if value.get('cache', {}).get('cache_option_table'):
                print 'cache_option_table:\n%s' % value['cache']['cache_option_table']
            print

def MEMCACHE_PRINT():
    pass


if globalconfig.get('memcache'):
    memcache.figlet()
    for instance in globalconfig.get('memcache'):
        print 'Server: %s' % instance
        print 'Version: %s' % globalconfig['memcache'][instance].get('version', '')
        print 'Bytes: %s' % globalconfig['memcache'][instance].get('bytes', '')
        print 'Bytes Read: %s' % globalconfig['memcache'][instance].get('bytes_read', '')
        print 'Bytes Written: %s' % globalconfig['memcache'][instance].get('bytes_written', '')
        print 'Current items: %s' % globalconfig['memcache'][instance].get('curr_items', '')
        print 'Evictions: %s' % globalconfig['memcache'][instance].get('evictions', '')
        print 'Get hits: %s' % globalconfig['memcache'][instance].get('get_hits', '')
        print 'Get misses: %s' % globalconfig['memcache'][instance].get('get_misses', '')
        print 'Limit MaxBytes: %s' % globalconfig['memcache'][instance].get('limit_maxbytes', '')
        print

def REDIS_PRINT():
    pass


if globalconfig.get('redis'):
    redis.figlet()
    for instance in globalconfig.get('redis'):
        print 'Server: %s' % instance
        print 'Used memory peak: %s' % globalconfig.get('redis', {}).get(instance, {}).get('Memory', {}).get('used_memory_peak_human')
        if globalconfig.get('redis', {}).get(instance, {}).get('Stats', {}).get('evicted_keys'):
            print 'Evicted keys: %s' % globalconfig.get('redis', {}).get(instance, {}).get('Stats', {}).get('evicted_keys')
        if globalconfig.get('redis', {}).get(instance, {}).get('Keyspace'):
            print 'Keyspace:'
            for key, value in globalconfig.get('redis', {}).get(instance, {}).get('Keyspace', {}).iteritems():
                print '%s: %s' % (key, value)

        print

print

class TODO(object):
    pass


if (not os.path.isfile(args.output) or args.force) and not args.jsonfile and JSON == True:
    globalconfig['errors'] = error_collection
    json_str = json.dumps(globalconfig)
    outfile = open(args.output, 'w')
    outfile.write(json_str)
    outfile.close()
if args.printglobalconfig:
    print "\n  ____ _       _           _  ____             __ _       \n / ___| | ___ | |__   __ _| |/ ___|___  _ __  / _(_) __ _ \n| |  _| |/ _ \\| '_ \\ / _` | | |   / _ \\| '_ \\| |_| |/ _` |\n| |_| | | (_) | |_) | (_| | | |__| (_) | | | |  _| | (_| |\n \\____|_|\\___/|_.__/ \\__,_|_|\\____\\___/|_| |_|_| |_|\\__, |\n                                                    |___/\n"
    pp.pprint(globalconfig)
if args.printjson and JSON == True:
    print json.dumps(globalconfig)