# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/dataObject.py
# Compiled at: 2019-09-07 09:47:22
# Size of source mod 2**32: 2128 bytes
from __future__ import absolute_import
from __future__ import print_function
from sqlobject import *
import sys, os
from six.moves import range

def Connect(backend, user, pw, host, port, db):
    """
    Initializes the connection.
    """
    db_filename = os.path.abspath('Epigrass.sqlite')
    if backend == 'sqlite':
        connection_string = 'sqlite:' + db_filename
    else:
        if backend == 'mysql':
            connection_string = '%s://%s:%s@%s:%s/%s' % (backend, user, pw, host, port, db)
        else:
            if backend == 'postgresql':
                connection_string = '%s://%s:%s@%s:%s/%s' % (backend, user, pw, host, port, db)
            else:
                sys.exit('Invalid Database Backend specified: %s' % backend)
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection.transaction()


class Site(SQLObject):

    class sqlmeta:
        name = 'site'
        lazyUpdate = True

    geocode = IntCol()
    time = IntCol()
    totpop = IntCol()
    name = UnicodeCol()
    lat = FloatCol()
    longit = FloatCol()


class Edge(SQLObject):
    source_code = IntCol()
    dest_code = IntCol()
    time = IntCol()
    ftheta = FloatCol()
    btheta = FloatCol()

    class sqlmeta:
        name = 'sitee'
        lazyUpdate = True


if __name__ == '__main__':
    Connect('mysql', 'root', 'mysql', 'localhost', 3306, 'epigrass')
    Site._table = 'testando'
    Site.createTable()
    Edge.createTable()
    dicin = {'geocode':0,  'time':0,  'name':'euheim',  'totpop':100,  'lat':10.1,  'longit':20.3}
    for i in range(1):
        pid = os.fork()
        if pid:
            continue
        Site(**dicin)
        Site._connection.commit()
        print('commit from process %d' % os.getpid())
        sys.exit()