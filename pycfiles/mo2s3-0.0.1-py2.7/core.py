# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo2s3/core.py
# Compiled at: 2012-06-11 11:52:06
from datetime import datetime
import ConfigParser, argparse, envoy, boto, os, sys, shutil
from boto.s3.key import Key
from mo2s3 import default_conf
cfg = ConfigParser.SafeConfigParser()
cfg_file = os.path.expanduser('~/.mo2s3.cfg')
if not os.path.isfile(cfg_file):
    with open(cfg_file, 'w') as (f):
        f.write(default_conf)
cfg.read(cfg_file)
parser = argparse.ArgumentParser(description='Backup and restore MongoDB with Amazon S3.')
parser.add_argument('action', help='configure/backup/restore FILENAME/delete FILENAME/list/drop', action='store')
parser.add_argument('--host', help='Optional MongoDB Host', default=cfg.get('mongodb', 'host'))
parser.add_argument('-u', '--username', help='Optional MongoDB username', default=cfg.get('mongodb', 'username'))
parser.add_argument('-p', '--password', help='Optional MongoDB password', default=cfg.get('mongodb', 'password'))
parser.add_argument('-d', '--db', help='Optional MongoDB database', default='')
parser.add_argument('-b', '--bucket', help='AWS S3 bucket', default=cfg.get('aws', 's3_bucket'))
parser.add_argument('-f', '--filename', help='File to delete/restore', default='')
parser.add_argument('-a', '--access-key', help='AWS access key', default=cfg.get('aws', 'access_key'))
parser.add_argument('-s', '--secret-key', help='AWS secret key', default=cfg.get('aws', 'secret_key'))

def make_mongo_params(args):
    mongo_params = ' --host ' + args['host']
    if args['username']:
        mongo_params += ' --username ' + args['username'] + ' --password ' + args['password']
    if args['db']:
        mongo_params += ' --db ' + args['db']
    return mongo_params


def main():
    args = vars(parser.parse_args())
    if args['action'] == 'configure':
        cfg_parser = ConfigParser.SafeConfigParser()
        cfg_parser.add_section('aws')
        cfg_parser.set('aws', 'access_key', raw_input('AWS Access Key: '))
        cfg_parser.set('aws', 'secret_key', raw_input('AWS Secret Key: '))
        cfg_parser.set('aws', 's3_bucket', raw_input('S3 Bucket Name: '))
        cfg_parser.add_section('mongodb')
        cfg_parser.set('mongodb', 'host', raw_input('MongoDB Host: '))
        cfg_parser.set('mongodb', 'username', raw_input('MongoDB Username: '))
        cfg_parser.set('mongodb', 'password', raw_input('MongoDB Password: '))
        cfg_parser.write(open(os.path.expanduser('~/.mo2s3.cfg'), 'w'))
        print 'Config written in %s' % os.path.expanduser('~/.mo2s3.cfg')
        sys.exit(0)
    if not args['access_key'] or not args['secret_key']:
        print "S3 credentials not set, run 'mo2s3 configure' or specify --access-key/--secret-key, 'mo2s3 -h' to show the help"
        sys.exit(0)
    conn = boto.connect_s3(args['access_key'], args['secret_key'])
    bucket = conn.create_bucket(args['bucket'])
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    print 'S3 Bucket: ' + args['bucket']
    if args['action'] == 'backup':
        print 'MongoDB: ' + args['host']
        dump_directory = 'mongodump_' + now
        mongo_cmd = 'mongodump' + make_mongo_params(args) + ' -o ' + dump_directory
        if not args['db']:
            mongo_cmd += ' --oplog'
        print mongo_cmd
        mongodump = envoy.run(mongo_cmd)
        if mongodump.status_code != 0:
            print mongodump.std_err
        print mongodump.std_out
        tar_filename = 'mongodump'
        if args['db']:
            tar_filename += '_' + args['db']
        tar_filename += '_' + now + '.tgz'
        tar = envoy.run('tar czf ' + tar_filename + ' ' + dump_directory)
        if tar.status_code != 0:
            print tar.std_err
        print tar.std_out
        k = Key(bucket)
        k.key = tar_filename
        k.set_contents_from_filename(tar_filename)
        print tar_filename + ' uploaded'
        os.remove(tar_filename)
        shutil.rmtree(dump_directory)
    elif args['action'] == 'list':
        for key in bucket.get_all_keys():
            print key.name

    elif args['action'] == 'drop':
        for key in bucket.get_all_keys():
            print 'deleting ' + key.name
            key.delete()

    elif args['action'] == 'delete':
        if not args['filename']:
            print "No filename specified (--filename), 'mo2s3 -h' to show the help"
            sys.exit(0)
        k = Key(bucket)
        k.key = args['filename']
        print 'deleting ' + args['filename']
        k.delete()
    elif args['action'] == 'restore':
        print 'MongoDB: ' + args['host']
        if not args['filename']:
            print "No filename specified (--filename), 'mo2s3 -h' to show the help"
            sys.exit(0)
        k = Key(bucket)
        k.key = args['filename']
        print 'restoring ' + args['filename']
        k.get_contents_to_filename(args['filename'])
        dump_date = args['filename'][-18:-4]
        tar = envoy.run('tar xvzf ' + args['filename'])
        if tar.status_code != 0:
            print tar.std_err
        print tar.std_out
        restore_cmd = 'mongorestore' + make_mongo_params(args) + ' mongodump_' + dump_date
        if args['db']:
            restore_cmd += '/' + args['db']
        else:
            restore_cmd += ' --oplogReplay'
        mongorestore = envoy.run(restore_cmd)
        if mongorestore.status_code != 0:
            print mongorestore.std_err
        print mongorestore.std_out
        shutil.rmtree('mongodump_' + dump_date)
        os.romve(args['filename'])


if __name__ == '__main__':
    main()