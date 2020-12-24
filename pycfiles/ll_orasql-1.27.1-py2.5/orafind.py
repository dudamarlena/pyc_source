# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ll/orasql/scripts/orafind.py
# Compiled at: 2009-03-27 10:38:34
import sys, os, optparse
from ll import orasql, astyle
s4warning = astyle.Style.fromenv('LL_ORASQL_REPRANSI_WARNING', 'red:black')
s4error = astyle.Style.fromenv('LL_ORASQL_REPRANSI_ERROR', 'red:black')
s4comment = astyle.Style.fromenv('LL_ORASQL_REPRANSI_COMMENT', 'black:black:bold')
s4addedfile = astyle.Style.fromenv('LL_ORASQL_REPRANSI_ADDEDFILE', 'black:green')
s4addedline = astyle.Style.fromenv('LL_ORASQL_REPRANSI_ADDEDLINE', 'green:black')
s4removedfile = astyle.Style.fromenv('LL_ORASQL_REPRANSI_REMOVEDFILE', 'black:red')
s4removedline = astyle.Style.fromenv('LL_ORASQL_REPRANSI_REMOVEDLINE', 'red:black')
s4changedfile = astyle.Style.fromenv('LL_ORASQL_REPRANSI_CHANGEDFILE', 'black:blue')
s4changedline = astyle.Style.fromenv('LL_ORASQL_REPRANSI_CHANGEDLINE', 'blue:black')
s4pos = astyle.Style.fromenv('LL_ORASQL_REPRANSI_POS', 'black:black:bold')
s4connectstring = astyle.Style.fromenv('LL_ORASQL_REPRANSI_CONNECTSTRING', 'yellow:black')
s4connid = astyle.Style.fromenv('LL_ORASQL_REPRANSI_NOTE', 'yellow:black:bold')
s4action = astyle.Style.fromenv('LL_ORASQL_REPRANSI_NOTE', 'magenta:black')
s4object = astyle.Style.fromenv('LL_ORASQL_REPRANSI_OBJECT', 'green:black')

def cs(connection):
    return s4connectstring(connection.connectstring())


def df(obj):
    return s4object(str(obj))


def connid(name):
    return s4connid('[%d]' % name)


def showcomment(out, *texts):
    out.writeln(s4comment('-- ', *texts))


def conflictmarker(prefix, *text):
    return astyle.style_default(s4error(prefix), ' ', *text)


def showreport(out, type, countcreate, countdrop, countcollision, countmerge, countmergeconflict):
    first = True
    data = (('added', countcreate), ('dropped', countdrop), ('collided', countcollision), ('merged', countmerge), ('mergeconflict', countmergeconflict))
    for (name, count) in data:
        if count:
            if first:
                out.write(' => ')
                first = False
            else:
                out.write('; ')
            if name in ('collided', 'mergeconflict'):
                cls = s4error
            else:
                cls = s4action
            if count > 1:
                msg = '%d %ss %s' % (count, type, name)
            else:
                msg = '1 %s %s' % (type, name)
            out.write(cls(msg))

    if first:
        out.write(' => identical')
    out.writeln()


def gettimestamp(obj, cursor, format):
    try:
        timestamp = obj.udate(cursor)
    except orasql.SQLObjectNotFoundError:
        return "doesn't exist"

    if timestamp is not None:
        timestamp = timestamp.strftime(format)
    else:
        timestamp = 'without timestamp'
    return timestamp


def main(args=None):
    colors = ('yes', 'no', 'auto')
    p = optparse.OptionParser(usage='usage: %prog [options] connectstring searchstring [table] [table] ...')
    p.add_option('-v', '--verbose', dest='verbose', help='Give a progress report?', default=False, action='store_true')
    p.add_option('-c', '--color', dest='color', help='Color output (%s)' % (', ').join(colors), default='auto', choices=colors)
    p.add_option('-i', '--ignore-case', dest='ignorecase', help='Ignore case distinctions?', default=False, action='store_true')
    p.add_option('-r', '--read-lobs', dest='readlobs', help='Read LOBs when printing records?', default=False, action='store_true')
    p.add_option('-e', '--encoding', dest='encoding', help='Encoding of the command line arguments', default='utf-8')
    (options, args) = p.parse_args(args)
    if len(args) < 2:
        p.error('incorrect number of arguments')
        return 1
    if options.color == 'yes':
        color = True
    elif options.color == 'no':
        color = False
    else:
        color = None
    stdout = astyle.Stream(sys.stdout, color)
    stderr = astyle.Stream(sys.stderr, color)
    connectstring = args[0].decode(options.encoding)
    searchstring = args[1].decode(options.encoding)
    if options.ignorecase:
        searchstring = searchstring.lower()
    searchstring = '%%%s%%' % searchstring.replace('%', '%%')
    tablenames = [ name.decode(options.encoding).lower() for name in args[2:] ]
    connection = orasql.connect(connectstring, readlobs=options.readlobs)
    c = connection.cursor()
    tables = list(connection.itertables())
    for (i, table) in enumerate(tables):
        skip = tablenames and table.name.lower() not in tablenames
        if options.verbose:
            msg = 'skipped' if skip else 'searching'
            stderr.writeln('orafind.py: ', df(table), ' #', str(i + 1), '/', str(len(tables)), ': ', msg)
        if not skip:
            where = []
            for col in table.itercolumns():
                datatype = col.datatype()
                if datatype == 'clob' or datatype.startswith('varchar2'):
                    if options.ignorecase:
                        where.append('lower(%s) like :searchstring' % col.name)
                    else:
                        where.append('%s like :searchstring' % col.name)

            if not where:
                continue
            query = 'select * from %s where %s' % (table.name, (' or ').join(where))
            print query
            c.execute(query, searchstring=searchstring)
            for r in c:
                stdout.writeln('orafind.py: in ', df(table), ': ', repr(r))

    return 0


if __name__ == '__main__':
    sys.exit(main())