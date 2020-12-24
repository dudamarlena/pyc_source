# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/scripts/common.py
# Compiled at: 2009-05-06 14:40:42
"""
Function shared between the scripts.

"""
__docformat__ = 'restructuredtext en'
from biblio.webquery.basewebquery import *
from config import *
try:
    from biblio.webquery import __version__ as script_version
except:
    script_version = 'unknown'

__all__ = [
 'script_version',
 'add_shared_options',
 'check_shared_options',
 'construct_webquery']

def add_shared_options(optparser):
    optparser.add_option('--debug', dest='debug', action='store_true', help='For errors, issue a full traceback instead of just a message.')
    optparser.add_option('--service', '-s', dest='webservice', help='The webservice to query. Choices are %s. The default is %s.' % (
     (', ').join([ '%s (%s)' % (s['id'], s['title']) for s in WEBSERVICES ]),
     DEFAULT_WEBSERVICE['id']), metavar='SERVICE', choices=WEBSERVICE_LOOKUP.keys(), default=DEFAULT_WEBSERVICE['id'])
    optparser.add_option('--key', '-k', dest='service_key', help='The access key for the webservice, if one is required.', metavar='KEY', default=None)
    return


def check_shared_options(options, optparser):
    serv = WEBSERVICE_LOOKUP.get(options.webservice, None)
    if not serv:
        optparser.error("Unrecognised webservice '%s'" % options.webservice)
    if issubclass(serv['ctor'], BaseKeyedWebQuery):
        if not options.service_key:
            optparser.error('%s webservice requires access key' % serv['title'])
    elif options.service_key:
        optparser.error('%s webservice does not require access key' % serv['title'])
    return


def construct_webquery(service, key):
    serv_cls = WEBSERVICE_LOOKUP[service]['ctor']
    if issubclass(serv_cls, BaseKeyedWebQuery):
        return serv_cls(key=key, timeout=5.0, limits=None)
    else:
        return serv_cls(timeout=5.0, limits=None)
    return


if __name__ == '__main__':
    main()