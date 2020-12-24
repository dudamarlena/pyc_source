# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/lobbyists/benchmark.py
# Compiled at: 2008-10-19 02:28:52
"""Internal benchmarking functions for the lobbyists package."""
from . import lobbyists
import time, sys

def _timed_func(func):

    def timer(*args):
        start = time.clock()
        result = func(*args)
        finish = time.clock()
        return (result, finish - start)

    return timer


def _parse_all(doc):
    return list(lobbyists.parse_filings(doc))


def _skip_import_list(record, con):
    return list()


def _skip_import(record, con):
    return


def time_parse(doc):
    """Parse all filing records in a lobbyist database and time it.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns a tuple. The first item is the time (in seconds) taken to
    parse the entire document, and the second is the list of all
    parsed filings.

    """
    timed_parser = _timed_func(_parse_all)
    return timed_parser(doc)


_skippers = {'registrant': _skip_import, 'client': _skip_import, 
   'lobbyists': _skip_import_list, 
   'govt_entities': _skip_import_list, 
   'issues': _skip_import_list, 
   'affiliated_orgs': _skip_import_list}

def time_import(cur, parsed_filings, skiplist=None):
    """Import parsed filings into a database and time it.

    cur - The DB API 2.0-compliant database cursor.

    parsed_filings - A sequence of parsed filings.

    skiplist - Either None (the default), or a list of filing element
    names ('registrant', 'client', etc.). Any filing element name that
    appears in the list is skipped at import time. This feature is
    useful for stubbing out specific import functions when you don't
    want them to impact the benchmark.

    Returns a tuple. The first item is the time (in seconds) taken by
    the import, and the second is the return value of
    lobbyist.import_filings.

    """
    if skiplist:
        for key in skiplist:
            lobbyists._entity_importers[key] = _skippers[key]

    timed_importer = _timed_func(lobbyists.import_filings)
    return timed_importer(cur, parsed_filings)


def main(argv=None):
    """Run the lobbyists-benchmark script directly from Python.

    Note that argv[0] is the program name.

    """
    import sqlite3, optparse, os.path
    if argv is None:
        argv = sys.argv
    usage = "%prog [OPTIONS] db doc.xml\n\nParse a Senate LD-1/LD-2 document, then import it into an sqlite3\ndatabase. Print the wall-clock time it takes to perform each action.\n\nThe document may be identified either by a URL or a file, so long as\nit's a valid Senate LD-1/LD-2 XML document.\n\nIf db doesn't exist, %prog will create it prior to importing the\ndocument."
    parser = optparse.OptionParser(usage=usage, version=lobbyists.VERSION)
    parser.add_option('-C', '--clobber-database', action='store_true', dest='clobber', help='clobber the existing database contents prior to loading first document')
    parser.add_option('-c', '--commit-database', action='store_true', dest='commit', help='commit the database after importing the document (default is not to commit)')
    parser.add_option('-s', '--skip-import', action='append', dest='skip_import', help='skip importing a particular entity, e.g., "registrant"')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) != 2:
        parser.error('specify one sqlite3 database and one XML document')
    (dbname, doc) = args
    create_db = options.clobber or not os.path.exists(dbname)
    con = sqlite3.connect(dbname)
    if create_db:
        lobbyists.create_db(con)
    (filings, parse_time) = time_parse(doc)
    print 'Parse time:', parse_time
    (_, import_time) = time_import(con.cursor(), filings, options.skip_import)
    print 'Import time:', import_time
    if options.commit:
        con.commit()
    con.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())