# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendeley2biblatex/library_converter.py
# Compiled at: 2016-07-11 07:11:10
# Size of source mod 2**32: 3994 bytes
import sqlite3, sys
from .bib_entry import BibEntry

def dict_factory(cursor, row):
    """A function to use the SQLite row as dict for string formatting"""
    d = {}
    for idx, col in enumerate(cursor.description):
        if row[idx]:
            d[col[0]] = row[idx]
        else:
            d[col[0]] = ''

    return d


class LibraryConverter:

    @staticmethod
    def convert_library(db_name, bibtex_file=sys.stdout, quiet=False, folder=None):
        """Converts Mendely SQlite database to BibTeX file
        @param db_name The Mendeley SQlite file
        @param bibtex_file The BibLaTeX file to output the bibliography, if not
    supplied the output is written to the system standard stdout.
        @param quiet If true do not show warnings and errors
        @param folder If provided the Rult gets filtered by folder name
        """
        db = sqlite3.connect(db_name)
        c = db.cursor()
        c.row_factory = dict_factory
        if sys.stdout != bibtex_file:
            f = open(bibtex_file, 'w')
            f.write('This file was generated automatically by Mendeley To\n    BibLaTeX python script.\n\n')
        else:
            f = bibtex_file
        query = '\n            SELECT\n            D.id,\n            D.citationKey,\n            D.title,\n            D.type,\n            D.doi,\n            D.publisher,\n            D.publication,\n            D.volume,\n            D.issue,\n            D.institution,\n            D.month,\n            D.year,\n            D.pages,\n            D.revisionNumber AS number,\n            D.sourceType,\n            DU.url,\n            D.dateAccessed AS urldate\n        FROM Documents D\n        LEFT JOIN DocumentCanonicalIds DCI\n            ON D.id = DCI.documentId\n        LEFT JOIN DocumentFiles DF\n            ON D.id = DF.documentId\n        LEFT JOIN DocumentUrls DU\n            ON DU.documentId = D.id\n        LEFT JOIN DocumentFolders DFO\n            ON D.id = DFO.documentId\n        LEFT JOIN Folders FO\n            ON DFO.folderId = FO.id\n        WHERE D.confirmed = "true"\n        AND D.deletionPending= "false"\n        '
        if folder is not None:
            query += 'AND FO.name="' + folder + '"'
        query += '\n        GROUP BY D.citationKey\n        ORDER BY D.citationKey\n        ;'
        for entry in c.execute(query):
            c2 = db.cursor()
            c2.execute('\n        SELECT lastName, firstNames\n        FROM DocumentContributors\n        WHERE documentId = ?\n        ORDER BY id', (entry['id'],))
            authors_list = c2.fetchall()
            authors = []
            for author in authors_list:
                authors.append(', '.join(author))

            entry['authors'] = ' and '.join(authors)
            if isinstance(entry['url'], bytes):
                entry['url'] = entry['url'].decode('UTF-8')
            BibEntry.clean_characters(entry)
            try:
                formatted_entry = BibEntry.TEMPLATES.get(entry['type']).format(entry=entry)
            except AttributeError:
                if not quiet:
                    print('Unhandled entry type {0}, please add your own template.'.format(entry['type']))
                continue

            f.write(formatted_entry)

        if sys.stdout != bibtex_file:
            f.close()