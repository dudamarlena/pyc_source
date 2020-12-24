# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/lobbyists/util.py
# Compiled at: 2008-10-19 02:28:52
"""Utility functions for the lobbyists package."""
from . import lobbyists
import sqlite3, os.path

def load_db(docs, dbname, clobber=False, commit_per_doc=False):
    """Load filing records from lobbyist documents into an sqlite3 database.

    Parses and imports filing records from one or more Senate
    LD-1/LD-2 XML documents into an sqlite3 database. Records are
    parsed and imported one at a time.

    docs - A sequence of URLs or filenames identifying the LD-1/LD-2
    XML documents load load.

    dbname - The filename of the sqlite3 database to load. If the
    database doesn't exist, load_db creates it.

    clobber - If True, and the database already exists, the database's
    contents will be clobbered prior to loading.

    commit_per_doc - If True, load_db will commit the changes to the
    database after loading each individual document. If False (the
    default), load_db only commits when the last document is
    loaded. Per-document committing ensures that successfully loaded
    documents are committed to the database in case of parsing or
    importing errors in subsequent documents, but is slower.

    This function has the side-effect of creating and/or modifying the
    database.

    Returns the database's sqlite3.Connection object.

    """
    create_db = clobber or not os.path.exists(dbname)
    con = sqlite3.connect(dbname)
    if create_db:
        lobbyists.create_db(con)
    for doc in docs:
        lobbyists.import_filings(con.cursor(), lobbyists.parse_filings(doc))
        if commit_per_doc:
            con.commit()

    if not commit_per_doc:
        con.commit()
    return con


def load_main(argv=None):
    """Run the lobbyists-load script directly from Python.

    Note that argv[0] is the program name.

    """
    import optparse, sys
    if argv is None:
        argv = sys.argv
    usage = "%prog [OPTIONS] db doc.xml ...\n\nParse one or more Senate LD-1/LD-2 XML documents and load them into an\nsqlite3 database.\n\nEach document may be identified either by a URL or a file, so long as\nit's a valid Senate LD-1/LD-2 XML document.\n\nIf db doesn't exist, %prog will create it prior to loading the first\ndocument."
    parser = optparse.OptionParser(usage=usage, version=lobbyists.VERSION)
    parser.add_option('-C', '--clobber-database', action='store_true', dest='clobber', help='clobber the existing database contents prior to loading first document')
    parser.add_option('-c', '--commit-per-document', action='store_true', dest='commit', help='commit changes to the database after importing each document (default is to commit only after all documents are imported)')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) < 2:
        parser.error('specify exactly one sqlite3 database and at least one XML document')
    con = load_db(args[1:], args[0], options.clobber, options.commit)
    con.close()
    return 0