# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/tools/gridscan_download.py
# Compiled at: 2008-02-15 09:40:27
import sys, urllib, urllib2, datetime, time
try:
    from pysqlite2 import dbapi2 as sqlite
    sqlite_present = True
except Exception, e:
    sqlite_present = False
    try:
        import sqlite3 as sqlite
        sqlite_present = True
    except:
        pass

def do_excuse(line):
    if line.find('Checking for OSG $OSG_GRID existence') >= 0:
        return True
    if line.find('Checking for OSG $WNTMP definition') >= 0:
        return True
    if line.find('Checking for MonALISA configuration') >= 0:
        return True
    if line.find('Checking for VDS mpiexec (OPTIONAL) existence: FAIL') >= 0:
        return True
    if line.find('Checking for VDS k.2 (OPTIONAL) existence') >= 0:
        return True
    if line.find('Checking for a valid proxy for') >= 0:
        return True
    if line.find('Checking for OSG $Monalisa_HOME definition') >= 0:
        return True
    if line.find('Checking for OSG $APP writability') >= 0:
        return True
    return False


schema = '\n    CREATE TABLE GridScan (\n        time timestamp,\n        sitename varchar(255),\n        pass boolean\n    )\n'
insert_sql_str = '\n    INSERT into GridScan VALUES (\n    ?, ?, ?\n    )\n'
list_tests_str = '\n    SELECT distinct time from GridScan WHERE\n    sitename=?\n'

def connect_sqlite():
    return sqlite.connect('gridscan.db')


def insert_test(conn, site, timestamp, status):
    curs = conn.cursor()
    curs.execute(insert_sql_str, (timestamp, site, status))
    conn.commit()


def test_time_list(conn, site):
    curs = conn.cursor()
    rows = curs.execute(list_tests_str, (site,)).fetchall()
    time_tuples = [ time.strptime(i[0], '%Y-%m-%d %H:%M:%S') for i in rows ]
    return [ datetime.datetime(*i[:6]) for i in time_tuples ]


gridscan_url = 'http://scan.grid.iu.edu/cgi-bin/get_grid_sv?'

def site_listing():
    query = urllib.urlencode({'get': 'set1'})
    doc = urllib2.urlopen(gridscan_url + query)
    retval = {}
    for line in doc:
        (id, site, ce) = line.split(',')
        retval[site] = id

    return retval


def test_listing(id):
    query = urllib.urlencode({'id': id, 'get': 'listing'})
    doc = urllib2.urlopen(gridscan_url + query)
    retval = []
    for line in doc:
        retval.append(line.strip())

    return retval


def test_status(id, testname):
    query = urllib.urlencode({'id': id, 'get': testname})
    doc = urllib2.urlopen(gridscan_url + query)
    for line in doc:
        if line.find('FAIL') >= 0 and not do_excuse(line):
            print line.strip()
            return False

    return True


def datetime_from_listing(name):
    (d, t) = name.split('.')[0].split('-')[-2:]
    return datetime.datetime(*time.strptime(d + t, '%Y%m%d%H%M%S')[0:6])


def main():
    if not sqlite_present:
        print >> sys.stderr, 'SQLite not present.'
        sys.exit(1)
    sites = site_listing()
    conn = connect_sqlite()
    for (site, id) in sites.items():
        print 'Uploading site %s.' % site
        listings = test_listing(id)
        times = test_time_list(conn, site)
        for listing in listings:
            d = datetime_from_listing(listing)
            if d in times:
                continue
            print 'New test: %s' % d.strftime('%Y%m%d %H:%M:%S')
            status = test_status(id, listing)
            insert_test(conn, site, d, status)


if __name__ == '__main__':
    main()