# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/macvendor/macvendor.py
# Compiled at: 2019-12-12 19:58:08
# Size of source mod 2**32: 5056 bytes
import argparse, sys, re, os
PATH = os.path.dirname(os.path.realpath(__file__))
VERSION = '1.0.12'

def checkMacAddr(addr):
    regexList = {
     re.compile('^([0-9a-f][0-9a-f]:){3}(ff:fe:)?([0-9a-f][0-9a-f]:){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f]-){3}(ff-fe-)?([0-9a-f][0-9a-f]-){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f]\\.){3}(ff\\.fe\\.)?([0-9a-f][0-9a-f]\\.){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f]){3}(fffe)?([0-9a-f][0-9a-f]){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f]:){3}([0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f]\\.){3}([0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f]-){3}([0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f][0-9a-f]:)([0-9a-f][0-9a-f]ff:)(fe[0-9a-f][0-9a-f]:)([0-9a-f][0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f][0-9a-f]\\.)([0-9a-f][0-9a-f]ff\\.)(fe[0-9a-f][0-9a-f]\\.)([0-9a-f][0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f][0-9a-f][0-9a-f]-)([0-9a-f][0-9a-f]ff-)(fe[0-9a-f][0-9a-f]-)([0-9a-f][0-9a-f][0-9a-f][0-9a-f])$', re.IGNORECASE)}
    for regex in regexList:
        if re.match(regex, addr) is not None:
            return True

    return False


def checkOUI(oui):
    regexList = {
     re.compile('^([0-9a-f][0-9a-f]:){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f]\\.){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f][0-9a-f]-){2}([0-9a-f][0-9a-f])$', re.IGNORECASE),
     re.compile('^([0-9a-f]){6}$', re.IGNORECASE)}
    for regex in regexList:
        if re.match(regex, oui) is not None:
            return True

    return False


def cleanAddr(addr):
    for ch in {':', '.', '-'}:
        if ch in addr:
            addr = addr.replace(ch, '')

    return addr.upper()


def macToOui(addr, prefix):
    return cleanAddr(addr)[0:prefix]


def getVendorFromFile(line):
    return line.split('\t')[1].replace('\n', '')


def lookup(addr, file, prefix=6):
    oui = macToOui(addr, prefix)
    test = [addr, '']
    with open(file, 'r') as (db):
        for line in db:
            if oui in line:
                if 'IEEE Registration Authority' in line:
                    test[1] += getVendorFromFile(line)
                    if cleanAddr(addr)[6:10] == 'FFFE':
                        if len(cleanAddr(addr)) == 16:
                            addr = cleanAddr(addr)[0:6] + cleanAddr(addr)[10:]
                    prefix24 = lookup(addr, '{}/data/prefix28'.format(PATH), 7) or ''
                    prefix28 = lookup(addr, '{}/data/prefix36'.format(PATH), 9) or ''
                    test[1] += ' - {} {}'.format(prefix24[1], prefix28[1])
                else:
                    test[1] += getVendorFromFile(line)

    return test


def getVendorList(plist):
    result = {}
    if type(plist) is list or type(plist) is tuple:
        for addr in plist:
            if checkMacAddr(addr) or checkOUI(addr):
                lookupData = lookup(addr, '{}/data/prefix24'.format(PATH))
                result[lookupData[0]] = lookupData[1]
            else:
                result[addr] = 'Invalide MAC or OUI format'

    else:
        raise Exception('argument for getvendorList() should be a list or a tuple')
    return result


def getVendor(p):
    if checkMacAddr(p) or checkOUI(p):
        return lookup(p, './data/prefix24')
    return [p, 'Invalide Mac or OUI format']


def formatTable(d):
    from tabulate import tabulate
    headers = [
     'Mac', 'Vendor']
    data = [(k, v) for k, v in d.items()]
    return tabulate(data, headers=headers, tablefmt='github')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help='Displays version information.', action='store_true')
    parser.add_argument('address', metavar='address', type=str, nargs='*', help='one or multiple valide MAC address or OUI to lookup')
    args = parser.parse_args()
    if args.address:
        print(formatTable(getVendorList(args.address)))
    if args.version:
        print('verion {}'.format(VERSION))


if __name__ == '__main__':
    main()