# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/provider.py
# Compiled at: 2011-04-23 08:43:29
from math import sqrt
from sqlite3 import connect, Row
from copy import copy

class PointProvider:
    MAX_RESULTS = 1000

    def __init__(self, filename, ctype, table):
        self.filterstack = []
        self.conn = connect(filename)
        self.conn.row_factory = Row
        self.conn.text_factory = str
        self.ctype = ctype
        self.cache_table = table
        self.filterstring = []
        self.filterargs = []
        self.conn.executescript('PRAGMA temp_store = MEMORY;PRAGMA synchronous=OFF;CREATE TABLE IF NOT EXISTS %s (%s);' % (
         self.cache_table, (', ').join('%s %s' % m for m in self.ctype.SQLROW.items())))
        self.check_table()
        self.conn.executescript('CREATE INDEX IF NOT EXISTS %(table)s_latlon ON %(table)s (lat ASC, lon ASC);CREATE INDEX IF NOT EXISTS %(table)s_name ON %(table)s (name ASC);CREATE INDEX IF NOT EXISTS %(table)s_fieldnote ON %(table)s (logas);' % {'table': self.cache_table})

    def check_table(self):
        c = self.conn.cursor()
        fields = copy(self.ctype.SQLROW)
        c.execute('PRAGMA TABLE_INFO(%s)' % self.cache_table)
        for row in c:
            if row[1] in fields:
                del fields[row[1]]

        for (name, type) in fields.items():
            cmd = 'ALTER TABLE %s ADD COLUMN %s %s' % (self.cache_table, name, type)
            print 'Updating your Database, adding Column %s to Table %s:\n%s' % (name, self.cache_table, cmd)
            c.execute(cmd)

        self.save()

    def get_table_info(self):
        c = self.conn.cursor()
        c.execute('PRAGMA TABLE_INFO(%s)' % self.cache_table)
        return c.fetchall()

    def save(self):
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def add_point(self, p, replace=False):
        if replace:
            self.conn.execute('INSERT OR REPLACE INTO %s (`%s`) VALUES (%s)' % (self.cache_table, ('`, `').join(self.ctype.SQLROW.keys()), (', ').join(':%s' % k for k in self.ctype.SQLROW.keys())), p.serialize())
            return
        else:
            c = self.conn.cursor()
            c.execute('SELECT found FROM %s WHERE name = ?' % self.cache_table, (p.name,))
            num = len(c.fetchall())
            existing = num == 1
            c.close()
            if existing:
                self.conn.execute('UPDATE %s SET found = ?, type = ?, lat = ?, lon = ?, status = ? WHERE name = ?' % self.cache_table, (p.found, p.type, p.lat, p.lon, p.status, p.name))
                return False
            self.conn.execute('INSERT INTO %s (`%s`) VALUES (%s)' % (self.cache_table, ('`, `').join(self.ctype.SQLROW.keys()), (', ').join(':%s' % k for k in self.ctype.SQLROW.keys())), p.serialize())
            return True
            return

    def get_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM %s' % self.cache_table)
        return self.pack_result(c)

    def get_by_query(self, query):
        c = self.conn.execute(query)
        return self.pack_result(c)

    def get_points(self, c1, c2):
        c = self.conn.execute('SELECT * FROM %s WHERE (lat BETWEEN ? AND ?) AND (lon BETWEEN ? AND ?)' % self.cache_table, (min(c1.lat, c2.lat), max(c1.lat, c2.lat), min(c1.lon, c2.lon), max(c1.lon, c2.lon)))
        return self.pack_result(c)

    def get_titles_and_names(self):
        c = self.conn.execute('SELECT name, title FROM %s' % self.cache_table)
        strings = []
        for row in c:
            strings.append(row['name'])
            strings.append(row['title'])

        c.close()
        return strings

    def get_new_fieldnotes_count(self):
        c = self.conn.execute('SELECT count(*) AS cnt FROM %s WHERE logas != %d' % (self.cache_table, self.ctype.LOG_NO_LOG))
        for row in c:
            return row['cnt']

        return 0

    def get_new_fieldnotes(self):
        c = self.conn.execute('SELECT * FROM %s WHERE logas != %d' % (self.cache_table, self.ctype.LOG_NO_LOG))
        return self.pack_result(c)

    def get_nearest_point_filter(self, center, c1, c2, found):
        filterstring = copy(self.filterstring)
        filterargs = copy(self.filterargs)
        filterstring.append('((lat BETWEEN ? AND ?) AND (lon BETWEEN ? AND ?))')
        filterargs.append(min(c1.lat, c2.lat))
        filterargs.append(max(c1.lat, c2.lat))
        filterargs.append(min(c1.lon, c2.lon))
        filterargs.append(max(c1.lon, c2.lon))
        if found == True:
            filterstring.append('(found = 1)')
        elif found == False:
            filterstring.append('(found = 0)')
        query = 'SELECT * FROM %s WHERE %s' % (self.cache_table, (' AND ').join(filterstring))
        c = self.conn.execute(query, tuple(filterargs))
        mindist = ()
        mindistrow = None
        for row in c:
            dist = sqrt((row['lat'] - center.lat) ** 2 + (row['lon'] - center.lon) ** 2)
            if dist < mindist:
                mindistrow = row
                mindist = dist

        if mindistrow == None:
            return
        else:
            coord = self.ctype(mindistrow['lat'], mindistrow['lon'], '', mindistrow)
            return coord

    def set_filter(self, found=None, has_details=None, owner_search='', name_search='', size=None, terrain=None, diff=None, ctype=None, adapt_filter=False, marked=None):
        filter = copy(locals())
        del filter['self']
        self.filter = filter
        if adapt_filter:
            filterstring = copy(self.filterstring)
            filterargs = copy(self.filterargs)
        else:
            filterstring = []
            filterargs = []
        if found == True:
            filterstring.append('(found = 1)')
        elif found == False:
            filterstring.append('(found = 0)')
        if marked == True:
            filterstring.append('(marked = 1)')
        elif marked == False:
            filterstring.append('(marked = 0)')
        if has_details == True:
            filterstring.append("(desc != '' or shortdesc != '')")
        elif has_details == False:
            filterstring.append("NOT (desc != '' or shortdesc != '')")
        if owner_search != None and len(owner_search) > 2:
            filterstring.append("(owner LIKE '%%%s%%')" % owner_search)
        if name_search != None and len(name_search) > 2:
            filterstring.append("((name LIKE '%%%s%%') OR (title LIKE '%%%s%%'))" % (name_search, name_search))
        if size != None:
            filterstring.append('(size IN (%s))' % (', ').join(str(b) for b in size))
        if terrain != None:
            if type(terrain) == tuple:
                filterstring.append('(terrain >= ?) AND (terrain <= ?)')
                filterargs.append(terrain[0] * 10)
                filterargs.append(terrain[1] * 10)
            elif type(terrain) == list:
                filterstring.append('(terrain IN (%s))' % (', ').join('?' for b in terrain))
                for b in terrain:
                    filterargs.append(b * 10)

        if diff != None:
            if type(diff) == tuple:
                filterstring.append('(difficulty >= ?) AND (difficulty <= ?)')
                filterargs.append(diff[0] * 10)
                filterargs.append(diff[1] * 10)
            elif type(diff) == list:
                filterstring.append('(difficulty IN (%s))' % (', ').join('?' for b in diff))
                for b in diff:
                    filterargs.append(b * 10)

        if ctype != None:
            if len(ctype) > 0:
                filterstring.append('(type IN (%s))' % (', ').join('?' for b in ctype))
                for b in ctype:
                    filterargs.append(b)

        if len(filterstring) == 0:
            filterstring.append('1')
        self.filterstring = filterstring
        self.filterargs = filterargs
        return

    def push_filter(self):
        self.filterstack.append((self.filterstring, self.filterargs))

    def pop_filter(self):
        (self.filterstring, self.filterargs) = self.filterstack.pop()

    def get_points_filter(self, location=None, found=None, max_results=None):
        filterstring = copy(self.filterstring)
        filterargs = copy(self.filterargs)
        if max_results == None:
            max_results = self.MAX_RESULTS
        if location != None:
            (c1, c2) = location
            filterstring.append('(lat BETWEEN ? AND ?) AND (lon BETWEEN ? AND ?)')
            filterargs.append(min(c1.lat, c2.lat))
            filterargs.append(max(c1.lat, c2.lat))
            filterargs.append(min(c1.lon, c2.lon))
            filterargs.append(max(c1.lon, c2.lon))
        if found == True:
            filterstring.append('(found = 1)')
        elif found == False:
            filterstring.append('(found = 0)')
        query = 'SELECT * FROM %s WHERE %s LIMIT %s' % (self.cache_table, (' AND ').join(filterstring), max_results)
        c = self.conn.execute(query, tuple(filterargs))
        return self.pack_result(c)

    def pack_result(self, cursor):
        points = [ self.ctype(None, None, None, row) for row in cursor ]
        cursor.close()
        return points

    def find_by_string(self, string):
        query = 'SELECT * FROM %s WHERE name LIKE ? OR title LIKE ? LIMIT 2' % self.cache_table
        c = self.conn.execute(query, (string, string))
        row = c.fetchone()
        coord = self.ctype(None, None, None, row)
        if c.fetchone() != None:
            return
        else:
            return coord

    def update_field(self, coordinate, field, newvalue, save=True):
        query = 'UPDATE %s SET %s = ? WHERE name = ?' % (self.cache_table, field)
        self.conn.execute(query, (newvalue, coordinate.name))
        if save:
            self.save()

    def get_by_name(self, gcname):
        query = 'SELECT * FROM %s WHERE name LIKE ? LIMIT 2' % self.cache_table
        c = self.conn.execute(query, (gcname,))
        row = c.fetchone()
        if row != None:
            coord = self.ctype(None, None, None, row)
            return coord
        else:
            return
            return

    def remove_geocaches(self, list):
        names = [ x.name for x in list if x.name != '' ]
        query = 'DELETE FROM %s WHERE name IN (%s)' % (self.cache_table, (',').join('?' for x in names))
        self.conn.execute(query, tuple(names))
        self.save()

    def optimize(self):
        self.conn.execute('VACUUM')