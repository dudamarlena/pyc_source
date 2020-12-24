# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/hstouch.py
# Compiled at: 2019-10-25 15:27:18
# Size of source mod 2**32: 6725 bytes
import sys
import os.path as op
import logging, h5pyd as h5py
if __name__ == '__main__':
    from config import Config
else:
    from .config import Config
cfg = Config()

def getFolder(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    dir = h5py.Folder(domain, endpoint=endpoint, username=username, password=password, bucket=bucket)
    return dir


def createFolder(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    owner = None
    if 'hs_owner' in cfg:
        owner = cfg['hs_owner']
    dir = h5py.Folder(domain, mode='x', endpoint=endpoint, username=username, password=password, bucket=bucket, owner=owner)
    return dir


def getFile(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    fh = h5py.File(domain, mode='r', endpoint=endpoint, username=username, password=password, bucket=bucket)
    return fh


def createFile(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    owner = None
    if 'hs_owner' in cfg:
        owner = cfg['hs_owner']
    fh = h5py.File(domain, mode='x', endpoint=endpoint, username=username, password=password, bucket=bucket, owner=owner)
    return fh


def touchDomain(domain):
    make_folder = False
    if domain[(-1)] == '/':
        make_folder = True
        domain = domain[:-1]
    else:
        parent_domain = op.dirname(domain)
        if parent_domain == '/':
            if cfg['hs_username'] != 'admin':
                sys.exit('Only admin user can create top-level domains')
            if not make_folder:
                sys.exit('Only folders can be created as a top-level domain')
            if len(domain) < 5:
                sys.exit('Top-level folders must be at least three characters')
        else:
            if not parent_domain.endswith('/'):
                parent_domain += '/'
            else:
                try:
                    getFolder(parent_domain)
                except IOError as oe:
                    try:
                        if oe.errno in (404, 410):
                            sys.exit('Parent domain: {} not found'.format(parent_domain))
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

                hdomain = None
                try:
                    hdomain = getFile(domain)
                except IOError as oe:
                    try:
                        if oe.errno in (404, 410):
                            pass
                        else:
                            sys.exit('Unexpected error: {}'.format(oe))
                    finally:
                        oe = None
                        del oe

                if hdomain:
                    if not make_folder:
                        try:
                            r = hdomain['/']
                            r.attrs['hstouch'] = 1
                            hdomain.close()
                        except IOError as oe:
                            try:
                                sys.exit('Got error updating domain: {}'.format(oe))
                            finally:
                                oe = None
                                del oe

                    else:
                        sys.exit('Can not update timestamp of folder object')
                    hdomain.close()
                else:
                    if not make_folder:
                        try:
                            fh = createFile(domain)
                            if cfg['verbose']:
                                print('domain created: {}, root id: {}'.format(domain, fh.id.id))
                            fh.close()
                        except IOError as oe:
                            try:
                                sys.exit('Got error updating domain: {}'.format(oe))
                            finally:
                                oe = None
                                del oe

                    else:
                        try:
                            fh = createFolder(domain + '/')
                            if cfg['verbose']:
                                print('folder created', domain + '/')
                            fh.close()
                        except IOError as oe:
                            try:
                                sys.exit('Got error updating domain: {}'.format(oe))
                            finally:
                                oe = None
                                del oe


def printUsage():
    print('usage: {} [-v] [-e endpoint] [-u username] [-p password] [-o owner] [--loglevel debug|info|warning|error] [--logfile <logfile>] [--bucket <bucket_name>] domains'.format(cfg['cmd']))
    print('example: {} -e  http://hsdshdflab.hdfgroup.org  /home/myfolder/emptydomain.h5'.format(cfg['cmd']))
    sys.exit()


def main():
    domains = []
    argn = 1
    loglevel = logging.ERROR
    logfname = None
    cfg['cmd'] = sys.argv[0].split('/')[(-1)]
    if cfg['cmd'].endswith('.py'):
        cfg['cmd'] = 'python ' + cfg['cmd']
    cfg['verbose'] = False
    while argn < len(sys.argv):
        arg = sys.argv[argn]
        val = None
        if len(sys.argv) > argn + 1:
            val = sys.argv[(argn + 1)]
        if arg in ('-h', '--help'):
            printUsage()
        elif arg in ('-v', '--verbose'):
            cfg['verbose'] = True
            argn += 1
        elif arg == '--loglevel':
            val = val.upper()
            if val == 'DEBUG':
                loglevel = logging.DEBUG
            else:
                if val == 'INFO':
                    loglevel = logging.INFO
                else:
                    if val in ('WARN', 'WARNING'):
                        loglevel = logging.WARNING
                    else:
                        if val == 'ERROR':
                            loglevel = logging.ERROR
                        else:
                            printUsage()
            argn += 2
        elif arg in ('-e', '--endpoint'):
            cfg['hs_endpoint'] = sys.argv[(argn + 1)]
            argn += 2
        elif arg in ('-u', '--username'):
            cfg['hs_username'] = sys.argv[(argn + 1)]
            argn += 2
        elif arg in ('-p', '--password'):
            cfg['hs_password'] = sys.argv[(argn + 1)]
            argn += 2
        elif arg in ('-b', '--bucket'):
            cfg['hs_bucket'] = val
            argn += 2
        elif arg in ('-o', '--owner'):
            cfg['hs_owner'] = sys.argv[(argn + 1)]
            argn += 2
        elif arg[0] == '-':
            printUsage()
        else:
            domains.append(arg)
            argn += 1

    if len(domains) == 0:
        printUsage()
    logging.basicConfig(filename=logfname, format='%(asctime)s %(message)s', level=loglevel)
    logging.debug('set log_level to {}'.format(loglevel))
    for domain in domains:
        if not domain.startswith('/'):
            sys.exit('domain: {} must start with a slash'.format(domain))
        touchDomain(domain)


if __name__ == '__main__':
    main()