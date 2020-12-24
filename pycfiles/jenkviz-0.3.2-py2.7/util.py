# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jenkviz/util.py
# Compiled at: 2012-01-31 04:51:00
__author__ = 'Benoit Delbosc'
__copyright__ = 'Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>'
import hashlib, re, logging
from urlparse import urlparse
import pkg_resources
from datetime import datetime

def get_version():
    """Retrun the package version."""
    return pkg_resources.get_distribution('jenkviz').version


def init_logging(options):
    if hasattr(logging, '_bb_init'):
        return
    level = logging.INFO
    if options.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S', filename=options.logfile, filemode='w')
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging._bb_init = True
    print 'Logging to ' + options.logfile


def md5sum(filename):
    f = open(filename)
    md5 = hashlib.md5()
    while True:
        data = f.read(8192)
        if not data:
            break
        md5.update(data)

    return md5.hexdigest()


def str2id(filename):
    return re.sub('[^a-zA-Z0-9_]', '_', filename)


class BaseFilter(object):
    """Base filter."""

    def __ror__(self, other):
        return other

    def __call__(self, other):
        return other | self


class truncate(BaseFilter):
    """Middle truncate string up to length."""

    def __init__(self, length=40, extra='...'):
        self.length = length
        self.extra = extra

    def __ror__(self, other):
        if len(other) > self.length:
            mid_size = (self.length - 3) / 2
            other = other[:mid_size] + self.extra + other[-mid_size:]
        return other


def duration_to_second(duration):
    """Convert jenkins duration into second"""
    if not duration:
        return None
    else:
        match = re.match('^(([0-9])+ hr)? ?(([0-9]+) min)? ?(([0-9\\.]+) sec)?$', duration)
        ret = 0
        if match and len(match.groups()) == 6:
            if match.group(2):
                ret += 3600 * int(match.group(2))
            if match.group(4):
                ret += 60 * int(match.group(4))
            if match.group(6):
                ret += int(float(match.group(6)))
        return ret


def time_to_datetime(str_time):
    if str_time:
        return datetime.strptime(str_time, '%b %d, %Y %I:%M:%S %p')
    else:
        return


def extract_token(text, tag_start, tag_end):
    """Extract a token from text, using the first occurence of
    tag_start and ending with tag_end. Return None if tags are not
    found."""
    start = text.find(tag_start)
    end = text.find(tag_end, start + len(tag_start))
    if start < 0 or end < 0:
        return None
    return text[start + len(tag_start):end]


def split_jenkins_url(url):
    """Return [server, path, base_path, job_name, build_number]"""
    u = urlparse(url)
    seg = [ i for i in u.path.split('/') if i ]
    build_number = seg[(-1)]
    build_name = seg[(-2)]
    base = '/' + ('/').join(seg[:-2])
    return [url[:-len(u.path)],
     u.path,
     base,
     build_name,
     build_number]