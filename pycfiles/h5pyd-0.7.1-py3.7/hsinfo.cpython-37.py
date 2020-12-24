# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/hsinfo.py
# Compiled at: 2019-10-28 23:49:18
# Size of source mod 2**32: 9066 bytes
import sys, logging, time
from datetime import datetime
import h5pyd
if __name__ == '__main__':
    from config import Config
else:
    from .config import Config
cfg = Config()

def printUsage():
    print('usage: {} [-h] [--loglevel debug|info|warning|error] [--logfile <logfile>] [-c oonf_file] [-e endpoint] [-u username] [-p password] [-b bucket] [domain]'.format(cfg['cmd']))
    print('example: {} -e http://data.hdfgroup.org:7253'.format(cfg['cmd']))
    print('')
    print('Options:')
    print('     -e | --endpoint <domain> :: The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org')
    print('     -u | --user <username>   :: User name credential')
    print('     -p | --password <password> :: Password credential')
    print('     -b | --bucket <bucket> :: bucket name')
    print('     -c | --conf <file.cnf>  :: A credential and config file')
    print('     -H | --human-readable :: with -v, print human readable sizes (e.g. 123M)')
    print('     --logfile <logfile> :: logfile path')
    print('     --loglevel debug|info|warning|error :: Change log level')
    print('     --bucket <bucket_name> :: Storage bucket')
    print('     -h | --help    :: This message.')
    sys.exit()


def getUpTime(start_time):
    now = int(time.time())
    sec = now - start_time
    days = sec // 86400
    sec -= 86400 * days
    hrs = sec // 3600
    sec -= 3600 * hrs
    mins = sec // 60
    sec -= 60 * mins
    if days:
        ret_str = '{} days, {} hours {} min {} sec'.format(days, hrs, mins, sec)
    else:
        if hrs:
            ret_str = '{} hours {} min {} sec'.format(hrs, mins, sec)
        else:
            if mins:
                ret_str = '{} min {} sec'.format(mins, sec)
            else:
                ret_str = '{} sec'.format(sec)
    return ret_str


def format_size(n):
    if n is None or n == ' ':
        return '        '
    else:
        symbol = ' '
        return cfg['human_readable'] or str(n)
    for s in ('B', 'K', 'M', 'G', 'T'):
        if n < 1024:
            symbol = s
            break
        n /= 1024

    if symbol == 'B':
        return '{:}B'.format(n)
    return '{:.1f}{}'.format(n, symbol)


def getServerInfo(cfg):
    """ get server state and print """
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    try:
        info = h5pyd.getServerInfo(username=username, password=password, endpoint=endpoint)
        print('server name: {}'.format(info['name']))
        if 'state' in info:
            print('server state: {}'.format(info['state']))
        else:
            print('endpoint: {}'.format(endpoint))
            print('username: {}'.format(info['username']))
            print('password: {}'.format(info['password']))
            if info['state'] == 'READY':
                home_folder = getHomeFolder()
                if home_folder:
                    print('home: {}'.format(home_folder))
            if 'hsds_version' in info:
                print('server version: {}'.format(info['hsds_version']))
            if 'node_count' in info:
                print('node count: {}'.format(info['node_count']))
            else:
                if 'h5serv_version' in info:
                    print('server version: {}'.format(info['h5serv_version']))
        if 'start_time' in info:
            uptime = getUpTime(info['start_time'])
            print('up: {}'.format(uptime))
        print('h5pyd version: {}'.format(h5pyd.version.version))
    except IOError as ioe:
        try:
            if ioe.errno == 401:
                print('username/password not valid for username: {}'.format(username))
            else:
                print('Error: {}'.format(ioe))
        finally:
            ioe = None
            del ioe


def getDomainInfo(domain, cfg):
    """ get info about the domain and print """
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    if domain.endswith('/'):
        is_folder = True
        obj_class = 'Folder'
    else:
        is_folder = False
        obj_class = 'Domain'
    try:
        if domain.endswith('/'):
            f = h5pyd.Folder(domain, mode='r', endpoint=endpoint, username=username, password=password,
              bucket=bucket,
              use_cache=True)
        else:
            f = h5pyd.File(domain, mode='r', endpoint=endpoint, username=username, password=password,
              bucket=bucket,
              use_cache=True)
    except IOError as oe:
        try:
            if oe.errno in (404, 410):
                sys.exit('domain: {} not found'.format(domain))
            else:
                if oe.errno == 401:
                    sys.exit('Authorization failure')
                else:
                    if oe.errno == 403:
                        sys.exit('Not allowed')
                    else:
                        sys.exit('Unexpected error: {}'.format(oe))
        finally:
            oe = None
            del oe

    timestamp = datetime.fromtimestamp(int(f.modified))
    if is_folder:
        print('folder: {}'.format(domain))
        print('    owner:           {}'.format(f.owner))
        print('    last modified:   {}'.format(timestamp))
    else:
        num_objects = f.num_groups + f.num_datatypes + f.num_datasets
        num_chunks = f.num_objects - num_objects
        print('domain: {}'.format(domain))
        print('    owner:           {}'.format(f.owner))
        print('    id:              {}'.format(f.id.id))
        print('    last modified:   {}'.format(timestamp))
        print('    total_size:      {}'.format(format_size(f.total_size)))
        print('    allocated_bytes: {}'.format(format_size(f.allocated_bytes)))
        print('    num objects:     {}'.format(num_objects))
        print('    num chunks:      {}'.format(num_chunks))
    f.close()


def getHomeFolder():
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    if not username:
        return
    dir = h5pyd.Folder('/home/', username=username, password=password, endpoint=endpoint)
    homefolder = None
    for name in dir:
        if username.startswith(name):
            path = '/home/' + name + '/'
            try:
                f = h5pyd.Folder(path, username=username, password=password, endpoint=endpoint)
            except IOError as ioe:
                try:
                    continue
                finally:
                    ioe = None
                    del ioe

            except Exception as e:
                try:
                    continue
                finally:
                    e = None
                    del e

            if f.owner == username:
                homefolder = path
            f.close()
            if homefolder:
                break

    dir.close()
    return homefolder


def main():
    argn = 1
    cfg['cmd'] = sys.argv[0].split('/')[(-1)]
    if cfg['cmd'].endswith('.py'):
        cfg['cmd'] = 'python ' + cfg['cmd']
    else:
        cfg['loglevel'] = logging.ERROR
        cfg['logfname'] = None
        cfg['human_readable'] = False
        domains = []
        while argn < len(sys.argv):
            arg = sys.argv[argn]
            val = None
            if len(sys.argv) > argn + 1:
                val = sys.argv[(argn + 1)]
            if arg == '--loglevel':
                val = val.upper()
                if val == 'DEBUG':
                    cfg['loglevel'] = logging.DEBUG
                else:
                    if val == 'INFO':
                        cfg['loglevel'] = logging.INFO
                    else:
                        if val in ('WARN', 'WARNING'):
                            cfg['loglevel'] = logging.WARNING
                        else:
                            if val == 'ERROR':
                                cfg['loglevel'] = logging.ERROR
                            else:
                                printUsage()
                argn += 2
            elif arg == '--logfile':
                cfg['logfname'] = val
                argn += 2
            elif arg in ('-h', '--help'):
                printUsage()
            elif arg in ('-e', '--endpoint'):
                cfg['hs_endpoint'] = val
                argn += 2
            elif arg in ('-u', '--username'):
                cfg['hs_username'] = val
                argn += 2
            elif arg in ('-p', '--password'):
                cfg['hs_password'] = val
                argn += 2
            elif arg in ('-b', '--bucket'):
                cfg['hs_bucket'] = val
                argn += 2
            elif arg == '-H':
                cfg['human_readable'] = True
                argn += 1
            else:
                domains.append(arg)
                argn += 1

        logging.basicConfig(filename=(cfg['logfname']), format='%(asctime)s %(message)s', level=(cfg['loglevel']))
        logging.debug('set log_level to {}'.format(cfg['loglevel']))
        endpoint = cfg['hs_endpoint']
        if endpoint:
            if endpoint[(-1)] == '/' or endpoint[:4] != 'http':
                print("WARNING: endpoint: {} doesn't appear to be valid".format(endpoint))
            domains or getServerInfo(cfg)
        else:
            for domain in domains:
                getDomainInfo(domain, cfg)


if __name__ == '__main__':
    main()