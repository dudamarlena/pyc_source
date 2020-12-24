# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pybagit/multichecksum.py
# Compiled at: 2014-11-17 12:53:59
__author__ = 'Andrew Hankinson (andrew.hankinson@mail.mcgill.ca)'
__version__ = '1.5'
__date__ = '2011'
__copyright__ = 'Creative Commons Attribution'
__license__ = 'The MIT License\n\n                Permission is hereby granted, free of charge, to any person obtaining a copy\n                of this software and associated documentation files (the "Software"), to deal\n                in the Software without restriction, including without limitation the rights\n                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n                copies of the Software, and to permit persons to whom the Software is\n                furnished to do so, subject to the following conditions:\n\n                The above copyright notice and this permission notice shall be included in\n                all copies or substantial portions of the Software.\n\n                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n                IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n                FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n                LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n                THE SOFTWARE.'
import multiprocessing
from optparse import OptionParser
import os, sys, hashlib, codecs, re
from pybagit.exceptions import *
HASHALG = 'sha1'
ENCODING = 'utf-8'

def write_manifest(datadir, encoding):
    bag_root = os.path.split(os.path.abspath(datadir))[0]
    manifest_file = ('manifest-{0}.txt').format(HASHALG)
    p = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    mapresult = p.map_async(csumfile, dirwalk(datadir)).get()
    p.close()
    p.join()
    mfile = codecs.open(os.path.join(bag_root, manifest_file), 'wb', encoding)
    for csum, cfile in mapresult:
        rp = os.path.relpath(cfile, bag_root)
        fl = ensure_unix_pathname(rp)
        mfile.write(('{0} {1}\n').format(csum, fl))

    mfile.close()


def dirwalk(datadir):
    datafiles = []
    for dirpath, dirnames, filenames in os.walk(('{0}').format(datadir)):
        for fn in filenames:
            datafiles.append(os.path.join(dirpath, fn))

    return datafiles


def csumfile(filename):
    """ Based on
        http://abstracthack.wordpress.com/2007/10/19/calculating-md5-checksum/
    """
    hashalg = getattr(hashlib, HASHALG)()
    blocksize = 65536

    def __upd(m, data):
        m.update(data)
        return m

    fd = open(filename, 'rb')
    try:
        contents = iter(lambda : fd.read(blocksize), '')
        m = reduce(__upd, contents, hashalg)
    finally:
        fd.close()

    return (
     m.hexdigest(), filename)


def ensure_unix_pathname(pathname):
    if sys.platform != 'win32':
        return pathname
    replace = re.compile('\\\\', re.UNICODE)
    fnm = re.sub(replace, '/', pathname)
    return fnm


if __name__ == '__main__':
    parser = OptionParser()
    usage = '%prog [options] arg1 arg2'
    parser.add_option('-a', '--algorithm', action='store', help='checksum algorithm to use (sha1|md5)')
    parser.add_option('-c', '--encoding', action='store', help='File encoding to write manifest')
    options, args = parser.parse_args()
    if options.algorithm:
        if options.algorithm not in ('md5', 'sha1'):
            raise BagCheckSumNotValid('You must specify either "md5" or "sha1" as the checksum algorithm')
        HASHALG = options.algorithm
    if options.encoding:
        ENCODING = options.encoding
    if len(args) < 1:
        parser.error('You must specify a data directory')
    write_manifest(args[0], ENCODING)