# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/hsacl.py
# Compiled at: 2019-10-25 15:27:18
# Size of source mod 2**32: 11785 bytes
import sys, logging, h5pyd
if __name__ == '__main__':
    from config import Config
else:
    from .config import Config
cfg = Config()

def getACL(f, username='default'):
    try:
        acl = f.getACL(username)
    except IOError as ioe:
        try:
            if ioe.errno == 403:
                print('No permission to read ACL for this domain')
                sys.exit(1)
            else:
                if ioe.errno == 401:
                    print('username/password needs to be provided')
                    sys.exit(1)
                else:
                    return ioe.errno == 404 or ioe.errno or None
                    print('unexpected error: {}'.format(ioe))
                    sys.exit(1)
        finally:
            ioe = None
            del ioe

    if acl:
        if 'domain' in acl:
            del acl['domain']
    return acl


def printUsage():
    print('')
    print('Usage: {} [options] domain [+crudep] [-crudep] [userid1 userid2 ...]'.format(cfg['cmd']))
    print('')
    print('Options:')
    print('     -v | --verbose :: verbose output')
    print('     -e | --endpoint <domain> :: The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org')
    print('     -u | --user <username>   :: User name credential')
    print('     -p | --password <password> :: Password credential')
    print('     --logfile <logfile> :: logfile path')
    print('     --loglevel debug|info|warning|error :: Change log level')
    print('     --bucket <bucket_name> :: Storage bucket')
    print('     -h | --help    :: This message.')
    print('Arguments:')
    print(' domain :: Domain or Folder to be updated')
    print(' +/- :: add or remove permissions')
    print(' crudep :: permission flags: Create, Read, Update, Delete, rEadacl, uPdateacl')
    print('')
    print('examples...')
    print('list acls: {} /home/jill/myfile.h5'.format(cfg['cmd']))
    print("list ted's acl (if any): {} /home/jill/myfile.h5  ted".format(cfg['cmd']))
    print('add/update acl to give ted read & update permissions: {} /home/jill/myfile.h5 +ru ted'.format(cfg['cmd']))
    print('remove all permissions except read for jill: {} /home/jill/myfile.h5 -cudep jill'.format(cfg['cmd']))
    print('')
    sys.exit()


def main():
    cfg['cmd'] = sys.argv[0].split('/')[(-1)]
    if cfg['cmd'].endswith('.py'):
        cfg['cmd'] = 'python ' + cfg['cmd']
    else:
        cfg['verbose'] = False
        perm_abvr = {'c':'create', 
         'r':'read',  'u':'update',  'd':'delete',  'e':'readACL',  'p':'updateACL'}
        fields = ('username', 'create', 'read', 'update', 'delete', 'readACL', 'updateACL')
        domain = None
        perm = None
        loglevel = logging.ERROR
        logfname = None
        usernames = []
        add_list = set()
        remove_list = set()
        if len(sys.argv) == 1 or sys.argv[1] == '-h':
            printUsage()
        logging.basicConfig(filename=logfname, format='%(asctime)s %(message)s', level=loglevel)
        logging.debug('set log_level to {}'.format(loglevel))
        argn = 1
        while argn < len(sys.argv):
            arg = sys.argv[argn]
            val = None
            if len(sys.argv) > argn + 1:
                val = sys.argv[(argn + 1)]
            logging.debug('arg:', arg, 'val:', val)
            if domain is None:
                if arg in ('-v', '--verbose'):
                    cfg['verbose'] = True
                    argn += 1
            if domain is None:
                if arg == '--loglevel':
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
            if domain is None:
                if arg == '--logfile':
                    logfname = val
                    argn += 2
            if domain is None:
                if arg in ('-h', '--help'):
                    printUsage()
            if domain is None and arg in ('-e', '--endpoint'):
                cfg['hs_endpoint'] = val
                argn += 2
            elif domain is None and arg in ('-u', '--username'):
                cfg['hs_username'] = val
                argn += 2
            elif domain is None and arg in ('-p', '--password'):
                cfg['hs_password'] = val
                argn += 2
            elif arg in ('-b', '--bucket'):
                cfg['hs_bucket'] = val
                argn += 2
            elif domain is None and arg[0] in ('-', '+'):
                print('No domain given')
                printUsage()
            elif domain is None:
                logging.debug('get domain')
                domain = arg
                if domain[0] != '/':
                    print("Domain must start with '/'")
                    printUsage()
                logging.debug('domain:', domain)
                argn += 1
            elif arg[0] == '+':
                logging.debug('got plus')
                if len(usernames) > 0:
                    logging.debug('usernames:', usernames)
                    printUsage()
                add_list = set(arg[1:])
                logging.info('add_list:', add_list)
                argn += 1
            elif arg[0] == '-':
                logging.debug('got minus')
                if len(usernames) > 0:
                    printUsage()
                remove_list = set(arg[1:])
                logging.info('remove_list:', remove_list)
                argn += 1
            else:
                logging.info('got username:', arg)
                if arg.find('/') >= 0:
                    print('Invalid username:', arg)
                    printUsage()
                usernames.append(arg)
                argn += 1

        logging.info('domain:', domain)
        logging.info('add_list:', add_list)
        logging.info('remove_list:', remove_list)
        logging.info('usernames:', usernames)
        if len(usernames) == 0 and not add_list:
            if remove_list:
                print('At least one username must be given to add/remove permissions')
                printUsage()
        if domain is None:
            print('no domain specified')
            sys.exit(1)
        conflicts = list(add_list & remove_list)
        if len(conflicts) > 0:
            print('permission: ', conflicts[0], ' permission flag set for both add and remove')
            sys.exit(1)
        mode = 'r'
        if not add_list:
            if remove_list:
                mode = 'a'
                perm = {}
                for x in add_list:
                    if x not in perm_abvr:
                        print("Permission flag: {} is not valid - must be one of 'crudep;".format(x))
                        sys.exit(1)
                    perm_name = perm_abvr[x]
                    perm[perm_name] = True

                for x in remove_list:
                    if x not in perm_abvr:
                        print("Permission flag: {} is not valid - must be one of 'crudep;".format(x))
                        sys.exit(1)
                    perm_name = perm_abvr[x]
                    perm[perm_name] = False

                logging.info('perm:', perm)
            try:
                if domain[(-1)] == '/':
                    f = h5pyd.Folder(domain, mode=mode, endpoint=(cfg['hs_endpoint']), username=(cfg['hs_username']), password=(cfg['hs_password']), bucket=(cfg['hs_bucket']))
                else:
                    f = h5pyd.File(domain, mode=mode, endpoint=(cfg['hs_endpoint']), username=(cfg['hs_username']), password=(cfg['hs_password']), bucket=(cfg['hs_bucket']))
            except IOError as ioe:
                try:
                    if ioe.errno in (404, 410):
                        print('domain not found')
                        sys.exit(1)
                    else:
                        if ioe.errno in (401, 403):
                            print('access is not authorized')
                            sys.exit(1)
                        else:
                            print('Unexpected error:', ioe)
                            sys.exit(1)
                finally:
                    ioe = None
                    del ioe

            if perm:
                default_acl = {'updateACL':False, 
                 'delete':False, 
                 'create':False, 
                 'read':False, 
                 'update':False, 
                 'readACL':False, 
                 'userName':'default'}
                update_names = []
                for username in usernames:
                    update_names.append(username)

                if not update_names:
                    update_names.append('default')
                for username in update_names:
                    acl = getACL(f, username=username)
                    if acl is None:
                        acl = default_acl.copy()
                    acl['userName'] = username
                    logging.info('updating acl to: {}'.format(acl))
                    for k in perm:
                        acl[k] = perm[k]

                    try:
                        f.putACL(acl)
                    except IOError as ioe:
                        try:
                            if ioe.errno in (401, 403):
                                print('access is not authorized')
                            else:
                                print('Unexpected error:', ioe)
                            sys.exit(1)
                        finally:
                            ioe = None
                            del ioe

            if len(usernames) == 0:
                try:
                    acls = f.getACLs()
                except IOError as ioe:
                    try:
                        if ioe.errno == 403:
                            print('User {} does not have permission to read ACL for this domain'.format(cfg['hs_username']))
                            sys.exit(1)
                        else:
                            if ioe.errno == 401:
                                print('username/password needs to be provided')
                                sys.exit(1)
                            else:
                                print('Unexpected error: {}'.format(ioe))
                    finally:
                        ioe = None
                        del ioe

                print('%015s   %08s  %08s  %08s  %08s  %08s  %08s ' % fields)
                print('--------------------------------------------------------------------------------')
                for acl in acls:
                    vals = (
                     acl['userName'], acl['create'], acl['read'], acl['update'], acl['delete'], acl['readACL'], acl['updateACL'])
                    print('%015s   %08s  %08s  %08s  %08s  %08s  %08s ' % vals)

        else:
            header_printed = False
            for username in usernames:
                try:
                    acl = f.getACL(username)
                    if not header_printed:
                        print('%015s   %08s  %08s  %08s  %08s  %08s  %08s ' % fields)
                        print('--------------------------------------------------------------------------------')
                        header_printed = True
                    vals = (
                     acl['userName'], acl['create'], acl['read'], acl['update'], acl['delete'], acl['readACL'], acl['updateACL'])
                    print('%015s   %08s  %08s  %08s  %08s  %08s  %08s ' % vals)
                except IOError as ioe:
                    try:
                        if ioe.errno == 403:
                            print('User {} does not have permission to read ACL for this domain'.format(cfg['hs_username']))
                            sys.exit(1)
                        else:
                            if ioe.errno == 401:
                                print('username/password needs to be provided')
                                sys.exit(1)
                            else:
                                if ioe.errno == 404:
                                    print(username, '<NONE>')
                                else:
                                    print('Unexpected error:', ioe)
                                    sys.exit(1)
                    finally:
                        ioe = None
                        del ioe

    f.close()


if __name__ == '__main__':
    main()