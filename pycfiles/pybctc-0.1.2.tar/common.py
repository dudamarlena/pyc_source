# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\yanglin\test/..\pybcs\common.py
# Compiled at: 2012-03-18 20:38:22
import urllib, urllib2, httplib, cookielib, os, re, sys, time, logging, hmac, base64, hashlib, commands, mimetypes
from cStringIO import StringIO
from urlparse import urlparse
from datetime import datetime

class FileSystemException(Exception):

    def __init__(self, msg=''):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return 'FileSystemException: ' + str(self.msg)


class NotImplementException(Exception):

    def __init__(self, msg=''):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return 'NotImplementException: ' + str(self.msg)


class bcolors:
    HEADER = '\x1b[95m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    ENDC = '\x1b[0m'

    def disable(self):
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''


def to_red(s):
    return bcolors.RED + str(s) + bcolors.ENDC


def to_yellow(s):
    return bcolors.YELLOW + str(s) + bcolors.ENDC


def to_green(s):
    return bcolors.GREEN + str(s) + bcolors.ENDC


def to_blue(s):
    return bcolors.BLUE + str(s) + bcolors.ENDC


def shorten(s, l=80):
    if len(s) <= l:
        return s
    return s[:l - 3] + '...'


def system(cmd):
    logging.info(cmd)
    r = commands.getoutput(cmd)
    logging.debug(r)
    return r


def md5_for_file(f, block_size=1048576):
    f = open(f, 'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)

    return md5.digest()


def parse_size(input):
    K = 1024
    M = K * K
    G = M * K
    T = G * K
    sizestr = re.search('(\\d*)', input).group(1)
    size = int(sizestr)
    if input.find('k') > 0 or input.find('K') > 0:
        size = size * K
    if input.find('m') > 0 or input.find('M') > 0:
        size = size * M
    if input.find('g') > 0 or input.find('G') > 0:
        size = size * G
    if input.find('t') > 0 or input.find('T') > 0:
        size = size * T
    return size


def format_size(input):
    input = int(input)
    K = 1024.0
    M = K * K
    G = M * K
    T = G * K
    if input >= T:
        return '%.2fT' % (input / T)
    if input >= G:
        return '%.2fG' % (input / G)
    if input >= M:
        return '%.2fM' % (input / M)
    if input >= K:
        return '%.2fK' % (input / K)
    return '%d' % input


def format_time(timestamp):
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    t = datetime.fromtimestamp(float(timestamp))
    return t.strftime(ISOTIMEFORMAT)


def init_logging(logger, set_level=logging.INFO, console=True, log_file_path=None):
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    for h in logger.handlers:
        logger.removeHandler(h)

    if console:
        fh = logging.StreamHandler()
        fh.setLevel(set_level)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if log_file_path:
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(set_level)
        formatter = logging.Formatter('%(asctime)-15s %(levelname)s  %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)