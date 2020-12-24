# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/scripts/queryisbn.py
# Compiled at: 2009-05-06 14:40:42
"""
Retreive bibliographic information for a given ISBN.

"""
__docformat__ = 'restructuredtext en'
import sys
from os import path
from optparse import OptionParser
from exceptions import BaseException
from config import *
from common import *
PRINT_FIELDS = [
 'title',
 'authors',
 'publisher',
 'year',
 'lang']
_DEV_MODE = False

def parse_args():
    usage = '%prog [options] ISBNs ...'
    version = 'version %s' % script_version
    epilog = ''
    description = 'Return bibliographic information from webservices for supplied ISBNs.'
    optparser = OptionParser(usage=usage, version=version, description=description, epilog=epilog)
    add_shared_options(optparser)
    (options, isbns) = optparser.parse_args()
    if not isbns:
        optparser.error('No ISBNs specified')
    check_shared_options(options, optparser)
    return (
     isbns, options)


def main():
    (isbn_list, options) = parse_args()
    webqry = construct_webquery(options.webservice, options.service_key)
    try:
        for isbn in isbn_list:
            print '%s:' % isbn
            rec_list = webqry.query_bibdata_by_isbn(isbn, format='bibrecord')
            if rec_list:
                for f in PRINT_FIELDS:
                    if getattr(rec_list[0], f):
                        print '   %s: %s' % (f, getattr(rec_list[0], f))

            else:
                print '   No results'

    except BaseException, err:
        if _DEV_MODE or options.debug:
            raise
        else:
            sys.exit(err)
    except:
        if _DEV_MODE or option.debug:
            raise
        else:
            sys.exit('An unknown error occurred.')


if __name__ == '__main__':
    main()