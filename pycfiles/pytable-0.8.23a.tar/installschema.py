# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/installschema.py
# Compiled at: 2008-02-14 08:23:38
"""Utility function to install pytable DBSchema in database"""
from pytable import sqlgeneration, sqlquery

def installSchema(connection, schema, users=(), ignoreErrors=0, pretend=False):
    """Install the given database schema's tables into database

        connection -- live connection to the database (that is, to
                the actual database into which the tables will be inserted)
        schema -- DatabaseSchema object to be created
        users -- sequence of "username" or "group username" sets
                defining the users who should be granted access to the
                created tables
        ignoreErrors -- if specified, don't raise errors, just print
                them to console.

        calls connection.commit() before returning
        returns None
        """
    driver = connection.driver
    creates = sqlgeneration.SQLCreateStatements(driver)(schema)
    if users:
        grants = sqlgeneration.SQLGrantStatements(driver, users=users)(schema)
        revokes = sqlgeneration.SQLRevokeStatements(driver, users=('PUBLIC', ))(schema)
    else:
        grants = []
        revokes = []
    executed = []
    cursor = connection.cursor()
    for query in getattr(schema, 'preCreationSQL', []) + creates + getattr(schema, 'postCreationSQL', []) + grants + revokes:
        if hasattr(query, 'split'):
            qSrc = [
             query]
        else:
            qSrc = query
        print ('\n').join([ [ line for line in q.split('\n') if line if isinstance(line, (str, unicode)) ][0] for q in qSrc
                          ])
        try:
            if not pretend:
                if isinstance(query, (list, tuple)):
                    for q in query:
                        cursor.execute(str(q))

                else:
                    cursor.execute(str(query))
            elif isinstance(query, (list, tuple)):
                for q in query:
                    print q

            else:
                print query
        except Exception:
            if ignoreErrors:
                print query
                traceback.print_exc()
            else:
                raise
        else:
            executed.append(query)

    if not pretend:
        connection.commit()
    else:
        connection.rollback()
    return executed