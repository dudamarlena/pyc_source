# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/hsls.py
# Compiled at: 2019-12-23 20:45:23
# Size of source mod 2**32: 16859 bytes
import sys
import os.path as op
import logging
from datetime import datetime
import h5pyd as h5py, numpy as np
if __name__ == '__main__':
    from config import Config
else:
    from .config import Config
cfg = Config()

def intToStr(n):
    if cfg['human_readable']:
        s = '{:,}'.format(n)
    else:
        s = '{}'.format(n)
    return s


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
        return '{:7}B'.format(n)
    return '{:7.1f}{}'.format(n, symbol)


def getShapeText(dset):
    shape_text = 'Scalar'
    shape = dset.shape
    if shape is not None:
        shape_text = '{'
        rank = len(shape)
        if rank == 0:
            shape_text += 'SCALAR'
        else:
            for dim in range(rank):
                if dim != 0:
                    shape_text += ', '
                shape_text += str(shape[dim])
                if cfg['verbose']:
                    max_extent = dset.maxshape[dim]
                    shape_text += '/'
                    if max_extent is None:
                        shape_text += 'Inf'
                    else:
                        shape_text += str(max_extent)

        shape_text += '}'
    return shape_text


def visititems(name, grp, visited):
    for k in grp:
        item = grp.get(k, getlink=True)
        class_name = item.__class__.__name__
        item_name = op.join(name, k)
        if class_name == 'HardLink':
            try:
                item = grp.get(k)
                dump(item_name, item, visited=visited)
            except IOError:
                desc = '{Missing hardlink object}'
                print('{0:24} {1} {2}'.format(item_name, class_name, desc))

        elif class_name == 'SoftLink':
            desc = '{' + item.path + '}'
            print('{0:24} {1} {2}'.format(item_name, class_name, desc))
        elif class_name == 'ExternalLink':
            desc = '{' + item.path + '//' + item.filename + '}'
            print('{0:24} {1} {2}'.format(item_name, class_name, desc))
        else:
            desc = '{Unknown Link Type}'
            print('{0:24} {1} {2}'.format(item_name, class_name, desc))


def getTypeStr(dt):
    return str(dt)


def dump(name, obj, visited=None):
    class_name = obj.__class__.__name__
    desc = None
    obj_id = None
    if class_name in ('Dataset', 'Group', 'Datatype', 'Table'):
        obj_id = obj.id.id
        if visited and obj_id in visited:
            same_as = visited[obj_id]
            print('{0:24} {1}, same as {2}'.format(name, class_name, same_as))
            return
    elif class_name in ('ExternalLink', 'SoftLink'):
        pass
    else:
        raise TypeError('unexpected classname: {}'.format(class_name))
    is_dataset = False
    if class_name in ('Dataset', 'Table'):
        is_dataset = True
    if is_dataset:
        desc = getShapeText(obj)
        obj_id = obj.id.id
    else:
        if class_name == 'Group':
            obj_id = obj.id.id
        else:
            if class_name == 'Datatype':
                obj_id = obj.id.id
            else:
                if class_name == 'SoftLink':
                    desc = '{' + obj.path + '}'
                else:
                    if class_name == 'ExternalLink':
                        desc = '{' + obj.filename + '//' + obj.path + '}'
                    else:
                        if desc is None:
                            print('{0} {1}'.format(name, class_name))
                        else:
                            print('{0} {1} {2}'.format(name, class_name, desc))
                        if cfg['verbose']:
                            if obj_id is not None:
                                print('    {0:>32}: {1}'.format('UUID', obj_id))
                        if cfg['verbose']:
                            if is_dataset:
                                if obj.shape is not None:
                                    if obj.chunks is not None:
                                        chunk_size = obj.dtype.itemsize
                                        if isinstance(obj.chunks, dict):
                                            chunk_dims = obj.chunks['dims']
                                            storage_desc = 'Storage ' + obj.chunks['class']
                                        else:
                                            chunk_dims = obj.chunks
                                            storage_desc = 'Storage H5D_CHUNKED'
                                        for chunk_dim in chunk_dims:
                                            chunk_size *= chunk_dim

                                        dset_size = obj.dtype.itemsize
                                        for dim_extent in obj.shape:
                                            dset_size *= dim_extent

                                        num_chunks = obj.num_chunks
                                        allocated_size = obj.allocated_size
                                        if num_chunks is not None and allocated_size is not None:
                                            fstr = '    {0:>32}: {1} {2} bytes, {3} allocated chunks'
                                            print(fstr.format('Chunks', chunk_dims, intToStr(chunk_size), intToStr(num_chunks)))
                                            if dset_size > 0:
                                                utilization = allocated_size / dset_size
                                                fstr = '    {0:>32}: {1} logical bytes, {2} allocated bytes, {3:.2f}% utilization'
                                                print(fstr.format(storage_desc, intToStr(dset_size), intToStr(allocated_size), utilization * 100.0))
                                            else:
                                                fstr = '    {0:>32}: {1} logical bytes, {2} allocated bytes'
                                                print(fstr.format(storage_desc, intToStr(dset_size), intToStr(allocated_size)))
                                        else:
                                            fstr = '    {0:>32}: {1} {2} bytes'
                                            print(fstr.format('Chunks', chunk_dims, intToStr(chunk_size)))
                                        fstr = '    {0:>32}: {1}'
                                        print(fstr.format('Type', getTypeStr(obj.dtype)))
                        if cfg['showattrs']:
                            if class_name in ('Dataset', 'Table', 'Group', 'Datatype'):
                                for attr_name in obj.attrs:
                                    attr = obj.attrs[attr_name]
                                    el = '...'
                                    if isinstance(attr, np.ndarray):
                                        rank = len(attr.shape)
                                    else:
                                        rank = 0
                                    if rank > 1:
                                        val = '[' * rank + el + ']' * rank
                                        print('   attr: {0:24} {1}'.format(attr_name, val))
                                    elif rank == 1 and attr.shape[0] > 1:
                                        val = '[{},{}]'.format(attr[0], el)
                                        print('   attr: {0:24} {1}'.format(attr_name, val))
                                    else:
                                        print('   attr: {0:24} {1}'.format(attr_name, attr))

                        if visited is not None:
                            if obj_id is not None:
                                visited[obj_id] = name
                        if class_name == 'Group' and visited is not None:
                            visititems(name, obj, visited)


def dumpACL(acl):
    perms = ''
    if acl['create']:
        perms += 'c'
    else:
        perms += '-'
    if acl['read']:
        perms += 'r'
    else:
        perms += '-'
    if acl['update']:
        perms += 'u'
    else:
        perms += '-'
    if acl['delete']:
        perms += 'd'
    else:
        perms += '-'
    if acl['readACL']:
        perms += 'e'
    else:
        perms += '-'
    if acl['updateACL']:
        perms += 'p'
    else:
        perms += '-'
    print('    acl: {0:24} {1}'.format(acl['userName'], perms))


def dumpAcls(obj):
    try:
        acls = obj.getACLs()
    except IOError:
        print('read ACLs is not permitted')
        return
    else:
        for acl in acls:
            dumpACL(acl)


def getFolder(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    pattern = cfg['pattern']
    query = cfg['query']
    batch_size = 100
    dir = h5py.Folder(domain, endpoint=endpoint, username=username, password=password,
      bucket=bucket,
      pattern=pattern,
      query=query,
      batch_size=batch_size)
    return dir


def getFile(domain):
    username = cfg['hs_username']
    password = cfg['hs_password']
    endpoint = cfg['hs_endpoint']
    bucket = cfg['hs_bucket']
    fh = h5py.File(domain, mode='r', endpoint=endpoint, username=username, password=password,
      bucket=bucket,
      use_cache=True)
    return fh


def visitDomains(domain, depth=1):
    if depth == 0:
        return 0
        count = 0
        if domain[(-1)] == '/':
            domain = domain[:-1]
    else:
        try:
            dir = getFolder(domain + '/')
            dir_class = 'domain'
            display_name = domain
            num_bytes = ' '
            if dir.is_folder:
                dir_class = 'folder'
                display_name += '/'
            else:
                if cfg['verbose']:
                    f = getFile(domain)
                    num_bytes = f.total_size
                    f.close()
                else:
                    owner = dir.owner
                    if owner is None:
                        owner = ''
                    if dir.modified is None:
                        timestamp = ''
                    else:
                        timestamp = datetime.fromtimestamp(int(dir.modified))
                print('{:15} {:15} {:8} {} {}'.format(owner, format_size(num_bytes), dir_class, timestamp, display_name))
                count += 1
                if cfg['showacls']:
                    dumpAcls(dir)
                for name in dir:
                    item = dir[name]
                    owner = item['owner']
                    full_path = domain + '/' + name
                    num_bytes = ' '
                    if cfg['verbose']:
                        if 'total_size' in item:
                            num_bytes = item['total_size']
                        else:
                            num_bytes = ' '
                        dir_class = item['class']
                        if item['lastModified'] is None:
                            timestamp = ''
                        else:
                            timestamp = datetime.fromtimestamp(int(item['lastModified']))
                        print('{:15} {:15} {:8} {} {}'.format(owner, format_size(num_bytes), dir_class, timestamp, full_path))
                        count += 1
                        if dir_class == 'folder':
                            n = visitDomains((domain + '/' + name), depth=(depth - 1))
                            count += n

        except IOError as oe:
            try:
                if oe.errno in (403, 404, 410):
                    pass
                else:
                    print('error getting domain:', domain)
                    sys.exit(str(oe))
            finally:
                oe = None
                del oe

    return count


def printUsage():
    print('usage: {} [-r] [-v] [-h] [--showacls] [--showattrs] [--loglevel debug|info|warning|error] [--logfile <logfile>] [-e endpoint] [-u username] [-p password] domains'.format(cfg['cmd']))
    print('example: {} -r -e http://hsdshdflab.hdfgroup.org /shared/tall.h5'.format(cfg['cmd']))
    print('')
    print('Options:')
    print('     -v | --verbose :: verbose output')
    print('     -H | --human-readable :: with -v, print human readable sizes (e.g. 123M)')
    print('     -e | --endpoint <domain> :: The HDF Server endpoint, e.g. http://hsdshdflab.hdfgroup.org')
    print('     -u | --user <username>   :: User name credential')
    print('     -p | --password <password> :: Password credential')
    print('     -c | --conf <file.cnf>  :: A credential and config file')
    print('     --showacls :: print domain ACLs')
    print('     --showattrs :: print attributes')
    print('     --pattern  :: <regex>  :: list domains that match the given regex')
    print('     --query :: <query> list domains where the attributes of the root group match the given query string')
    print('     --logfile <logfile> :: logfile path')
    print('     --loglevel debug|info|warning|error :: Change log level')
    print('     --bucket <bucket_name> :: Storage bucket')
    print('     -h | --help    :: This message.')
    sys.exit()


def main():
    domains = []
    argn = 1
    depth = 1
    loglevel = logging.ERROR
    logfname = None
    cfg['verbose'] = False
    cfg['showacls'] = False
    cfg['showattrs'] = False
    cfg['human_readable'] = False
    cfg['pattern'] = None
    cfg['query'] = None
    cfg['cmd'] = sys.argv[0].split('/')[(-1)]
    if cfg['cmd'].endswith('.py'):
        cfg['cmd'] = 'python ' + cfg['cmd']
    while argn < len(sys.argv):
        arg = sys.argv[argn]
        val = None
        if len(sys.argv) > argn + 1:
            val = sys.argv[(argn + 1)]
        if arg in ('-r', '--recursive'):
            depth = -1
            argn += 1
        elif arg in ('-v', '--verbose'):
            cfg['verbose'] = True
            argn += 1
        elif arg in ('-H', '--human-readable'):
            cfg['human_readable'] = True
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
        elif arg == '--logfile':
            logfname = val
            argn += 2
        elif arg in ('-showacls', '--showacls'):
            cfg['showacls'] = True
            argn += 1
        elif arg in ('-showattrs', '--showattrs'):
            cfg['showattrs'] = True
            argn += 1
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
        elif arg == '--pattern':
            cfg['pattern'] = val
            argn += 2
        elif arg == '--query':
            cfg['query'] = val
            argn += 2
        elif arg[0] == '-':
            printUsage()
        else:
            domains.append(arg)
            argn += 1

    logging.basicConfig(filename=logfname, format='%(asctime)s %(message)s', level=loglevel)
    logging.debug('set log_level to {}'.format(loglevel))
    if len(domains) == 0:
        domains.append('/')
    for domain in domains:
        if domain.endswith('/'):
            count = visitDomains(domain, depth=depth)
            print('{} items'.format(count))
        else:
            try:
                f = getFile(domain)
            except IOError as ioe:
                try:
                    if ioe.errno == 401:
                        print('Username/Password missing or invalid')
                        continue
                    elif ioe.errno == 403:
                        print('No permission to read domain: {}'.format(domain))
                        continue
                    else:
                        if ioe.errno == 404:
                            print('Domain {} not found'.format(domain))
                            continue
                        else:
                            if ioe.errno == 410:
                                print('Domain {} has been removed'.format(domain))
                                continue
                            else:
                                print('Unexpected error: {}'.format(ioe))
                                continue
                finally:
                    ioe = None
                    del ioe

            grp = f['/']
            if grp is None:
                print('{}: No such domain'.format(domain))
                domain += '/'
                count = visitDomains(domain, depth=depth)
                print('{} items'.format(count))
                continue
            else:
                dump('/', grp)
                if depth < 0:
                    visited = {}
                    visited[grp.id.id] = '/'
                    visititems('/', grp, visited)
                else:
                    for k in grp:
                        item = grp.get(k, getlink=True)
                        if item.__class__.__name__ == 'HardLink':
                            try:
                                item = grp[k]
                            except IOError:
                                pass

                        dump(k, item)

            if cfg['showacls']:
                dumpAcls(grp)
            grp.file.close()


if __name__ == '__main__':
    main()