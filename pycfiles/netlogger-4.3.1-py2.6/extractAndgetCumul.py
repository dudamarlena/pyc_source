# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/pegasus/extractAndgetCumul.py
# Compiled at: 2009-12-08 17:43:30
import nl_troubleshooting

def getGuids(dbname):
    c = nl_troubleshooting.getConnection(dbname)
    c.execute("select distinct value from ident where name = 'guid';")
    res = c.fetchall()
    return [ r[0] for r in res ]


def buildIndivTables(dbname, guid, tname):
    c = nl_troubleshooting.getConnection(dbname)
    if guid != None:
        c.execute("select min(e_id), max(e_id) from ident where name = 'guid' and value = '%s';" % guid)
    else:
        c.execute('select min(e_id), max(e_id) from ident;' % guid)
    vals = c.fetchall()[0]
    c.execute("select * from event where id >= %s and id <= %s and name = 'pegasus.invocation' into outfile '/tmp/scec.out.event%s';" % (vals[0], vals[1], tname))
    c.execute("select * from ident where e_id >= %s and e_id <= %s and name = 'p' into outfile '/tmp/scec.out.ident%s';" % (vals[0], vals[1], tname))
    c.execute("select * from attr where e_id >= %s and e_id <= %s and name = 'duration' into outfile '/tmp/scec.out.attr%s';" % (vals[0], vals[1], tname))
    c.execute('create table event%s select * from event limit 1,1;' % tname)
    c.execute('create table ident%s select * from ident limit 1,1;' % tname)
    c.execute('create table attr%s select * from attr limit 1,1;' % tname)
    c.execute('delete from event%s' % tname)
    c.execute('delete from ident%s' % tname)
    c.execute('delete from attr%s' % tname)
    c.execute("load data local infile '/tmp/scec.out.event%s' into table event%s;" % (tname, tname))
    c.execute("load data local infile '/tmp/scec.out.ident%s' into table ident%s;" % (tname, tname))
    c.execute("load data local infile '/tmp/scec.out.attr%s' into table attr%s;" % (tname, tname))
    c.execute('create index eidindex on ident%s(e_id)' % tname)
    c.execute('create index eidindex on attr%s(e_id)' % tname)
    return


def createDurationTable(dbname, tname):
    c = nl_troubleshooting.getConnection(dbname)
    c.execute('select distinct value from ident%s;' % tname)
    res = c.fetchall()
    pids = [ r[0] for r in res ]
    print 'got PIDs'
    c.execute('select ident%s.e_id, ident%s.value, attr%s.value from ident%s join attr%s on ident%s.e_iyd = attr%s.e_id' % (tname, tname, tname, tname, tname, tname, tname))
    print 'join complete'
    rows = c.fetchall()
    newrows = []
    for pid in pids:
        subrow = [ item for item in rows if item[1] == pid ]
        total = 0
        for i in range(len(subrow)):
            total += float(subrow[i][2])
            subrow[i] = subrow[i] + (total,)

        newrows += subrow

    f = file('/tmp/cumulative%s' % tname, 'w')
    f.write(('').join([ '%s\t%s\t%s\t%s\n' % (row[0], row[1], row[2], row[3]) for row in newrows ]))
    print 'cums calculated'
    c.execute('create table cumulative%s (e_id int, pid char(6), time float, cum float);' % tname)
    c.execute("load data local infile '/tmp/cumulative%s' into table cumulative%s;" % (tname, tname))


def main():
    guids = getGuids('foo')
    for g in guids:
        buildIndivTables('foo', g, g[-2:])
        createDurationTable('foo', g[-2:])


if __name__ == '__main__':
    main()