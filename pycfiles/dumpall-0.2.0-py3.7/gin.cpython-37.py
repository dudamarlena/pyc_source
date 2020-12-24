# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/thirdparty/gin.py
# Compiled at: 2019-10-23 04:38:54
# Size of source mod 2**32: 7328 bytes
"""gin - a Git index file parser"""
version = '0.1.006'
import binascii, collections, json, mmap, struct

def check(boolean, message):
    if not boolean:
        import sys
        print(('error: ' + message), file=(sys.stderr))
        sys.exit(1)


def parse(filename, pretty=True):
    with open(filename, 'rb') as (o):
        f = mmap.mmap((o.fileno()), 0, prot=(mmap.PROT_READ))

        def read(format):
            format = '! ' + format
            bytes = f.read(struct.calcsize(format))
            return struct.unpack(format, bytes)[0]

        index = collections.OrderedDict()
        index['signature'] = f.read(4).decode('ascii')
        check(index['signature'] == 'DIRC', 'Not a Git index file')
        index['version'] = read('I')
        check(index['version'] in {2, 3}, 'Unsupported version: %s' % index['version'])
        index['entries'] = read('I')
        yield index
        for n in range(index['entries']):
            entry = collections.OrderedDict()
            entry['entry'] = n + 1
            entry['ctime_seconds'] = read('I')
            entry['ctime_nanoseconds'] = read('I')
            if pretty:
                entry['ctime'] = entry['ctime_seconds']
                entry['ctime'] += entry['ctime_nanoseconds'] / 1000000000
                del entry['ctime_seconds']
                del entry['ctime_nanoseconds']
            entry['mtime_seconds'] = read('I')
            entry['mtime_nanoseconds'] = read('I')
            if pretty:
                entry['mtime'] = entry['mtime_seconds']
                entry['mtime'] += entry['mtime_nanoseconds'] / 1000000000
                del entry['mtime_seconds']
                del entry['mtime_nanoseconds']
            entry['dev'] = read('I')
            entry['ino'] = read('I')
            entry['mode'] = read('I')
            if pretty:
                entry['mode'] = '%06o' % entry['mode']
            entry['uid'] = read('I')
            entry['gid'] = read('I')
            entry['size'] = read('I')
            entry['sha1'] = binascii.hexlify(f.read(20)).decode('ascii')
            entry['flags'] = read('H')
            entry['assume-valid'] = bool(entry['flags'] & 32768)
            entry['extended'] = bool(entry['flags'] & 16384)
            stage_one = bool(entry['flags'] & 8192)
            stage_two = bool(entry['flags'] & 4096)
            entry['stage'] = (stage_one, stage_two)
            namelen = entry['flags'] & 4095
            entrylen = 62
            if entry['extended']:
                if index['version'] == 3:
                    entry['extra-flags'] = read('H')
                    entry['reserved'] = bool(entry['extra-flags'] & 32768)
                    entry['skip-worktree'] = bool(entry['extra-flags'] & 16384)
                    entry['intent-to-add'] = bool(entry['extra-flags'] & 8192)
                    entrylen += 2
            if namelen < 4095:
                entry['name'] = f.read(namelen).decode('utf-8', 'replace')
                entrylen += namelen
            else:
                name = []
                while True:
                    byte = f.read(1)
                    if byte == '\x00':
                        break
                    name.append(byte)

                entry['name'] = (b'').join(name).decode('utf-8', 'replace')
                entrylen += 1
            padlen = 8 - entrylen % 8 or 8
            nuls = f.read(padlen)
            check(set(nuls) == {0}, 'padding contained non-NUL')
            yield entry

        indexlen = len(f)
        extnumber = 1
        while f.tell() < indexlen - 20:
            extension = collections.OrderedDict()
            extension['extension'] = extnumber
            extension['signature'] = f.read(4).decode('ascii')
            extension['size'] = read('I')
            extension['data'] = f.read(extension['size'])
            extension['data'] = extension['data'].decode('iso-8859-1')
            if pretty:
                extension['data'] = json.dumps(extension['data'])
            yield extension
            extnumber += 1

        checksum = collections.OrderedDict()
        checksum['checksum'] = True
        checksum['sha1'] = binascii.hexlify(f.read(20)).decode('ascii')
        yield checksum
        f.close()


def parse_file(arg, pretty=True):
    if pretty:
        properties = {'version':'[header]',  'entry':'[entry]', 
         'extension':'[extension]', 
         'checksum':'[checksum]'}
    else:
        print('[')
    for item in parse(arg, pretty=pretty):
        if pretty:
            for key, value in properties.items():
                if key in item:
                    print(value)
                    break
            else:
                print('[?]')

            if pretty:
                for key, value in item.items():
                    print(' ', key, '=', value)

            else:
                print(json.dumps(item))
            last = 'checksum' in item
            if last or pretty:
                print()
            else:
                print(',')

    if not pretty:
        print(']')


def main():
    import argparse, os.path, sys
    parser = argparse.ArgumentParser(description='parse a Git index file')
    parser.add_argument('-j', '--json', action='store_true', help='output JSON')
    parser.add_argument('-v',
      '--version', action='store_true', help='show script version number')
    parser.add_argument('path',
      nargs='?', default='.', help='path to a Git repository or index file')
    args = parser.parse_args()
    if args.version:
        print('gin ' + version)
        sys.exit()
    elif os.path.isdir(args.path):
        path = os.path.join(args.path, '.git', 'index')
        if os.path.isfile(path):
            args.path = path
        else:
            print("error: couldn't find a .git/index file to use", file=(sys.stderr))
            print('use -h or --help for some documentation', file=(sys.stderr))
            sys.exit(1)
    if not args.path:
        parser.print_usage()
        sys.exit(2)
    parse_file((args.path), pretty=(not args.json))


if __name__ == '__main__':
    main()