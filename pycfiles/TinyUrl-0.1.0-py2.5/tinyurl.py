# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tinyurl.py
# Compiled at: 2009-01-08 11:51:50
"""A really tiny interface to ``tinyurl.com``."""
import sys, urllib, optparse
API_CREATE = 'http://tinyurl.com/api-create.php'
DEFAULT_DELIM = '\n'
USAGE = '%prog [options] url [url url ...]\n\n' + __doc__ + '\nAny number of urls may be passed and will be returned\nin order with the given delimiter, default=%r\n' % DEFAULT_DELIM
ALL_OPTIONS = (
 (
  ('-d', '--delimiter'),
  dict(dest='delimiter', default=DEFAULT_DELIM, help='delimiter for returned results')),)

def _build_option_parser():
    prs = optparse.OptionParser(usage=USAGE)
    for (args, kwargs) in ALL_OPTIONS:
        prs.add_option(*args, **kwargs)

    return prs


def create_one(url):
    url_data = urllib.urlencode(dict(url=url))
    ret = urllib.urlopen(API_CREATE, data=url_data).read().strip()
    return ret


def create(*urls):
    for url in urls:
        yield create_one(url)


def main(sysargs=sys.argv[:]):
    parser = _build_option_parser()
    (opts, urls) = parser.parse_args(sysargs[1:])
    for url in create(*urls):
        sys.stdout.write(url + opts.delimiter)

    return 0


if __name__ == '__main__':
    sys.exit(main())