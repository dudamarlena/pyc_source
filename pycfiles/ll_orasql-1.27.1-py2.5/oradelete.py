# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ll/orasql/scripts/oradelete.py
# Compiled at: 2009-03-31 13:38:00
import sys, os, optparse
from ll import astyle, orasql
s4warning = astyle.Style.fromenv('LL_ORASQL_REPRANSI_WARNING', 'red:black')
s4error = astyle.Style.fromenv('LL_ORASQL_REPRANSI_ERROR', 'red:black')
s4connectstring = astyle.Style.fromenv('LL_ORASQL_REPRANSI_CONNECTSTRING', 'yellow:black')
s4object = astyle.Style.fromenv('LL_ORASQL_REPRANSI_OBJECT', 'green:black')

def main(args=None):
    colors = ('yes', 'no', 'auto')
    fks = ('keep', 'disable', 'drop')
    p = optparse.OptionParser(usage='usage: %prog [options] connectstring >output.sql')
    p.add_option('-v', '--verbose', dest='verbose', help='Give a progress report?', default=False, action='store_true')
    p.add_option('-c', '--color', dest='color', help='Color output (%s)' % (', ').join(colors), default='auto', choices=colors)
    p.add_option('-s', '--sequences', dest='sequences', help='Should sequences be reset?', default=False, action='store_true')
    p.add_option('-x', '--execute', dest='execute', action='store_true', help='immediately execute the commands instead of printing them?')
    p.add_option('-i', '--ignore', dest='ignore', help='Ignore errors?', default=False, action='store_true')
    p.add_option('-e', '--encoding', dest='encoding', help='Encoding for output', default='utf-8')
    p.add_option('-t', '--truncate', dest='truncate', help='Truncate tables instead of deleting', default=False, action='store_true')
    (options, args) = p.parse_args(args)
    if len(args) != 1:
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
    connection = orasql.connect(args[0])
    cursor = connection.cursor()
    cs = s4connectstring(connection.connectstring())
    for (i, obj) in enumerate(connection.itertables(schema='user', mode='drop')):
        if options.verbose:
            msg = 'truncating' if options.truncate else 'deleting from'
            msg = astyle.style_default('oradelete.py: ', cs, ': %s #%d ' % (msg, i + 1), s4object(str(obj)))
            stderr.writeln(msg)
        if options.execute:
            try:
                if options.truncate:
                    cursor.execute('truncate table %s' % obj.name)
                else:
                    cursor.execute('delete from %s' % obj.name)
            except orasql.DatabaseError, exc:
                if not options.ignore or 'ORA-01013' in str(exc):
                    raise
                stderr.writeln('oradelete.py: ', s4error('%s: %s' % (exc.__class__, str(exc).strip())))

        else:
            if options.truncate:
                sql = 'truncate table %s;\n' % obj.name
            else:
                sql = 'delete from %s;\n' % obj.name
            stdout.write(sql.encode(options.encoding))

    if not options.truncate:
        connection.commit()
    if options.sequences:
        for (i, obj) in enumerate(connection.itersequences(schema='user')):
            if options.verbose:
                msg = astyle.style_default('oradelete.py: ', cs, ': recreating #%d ' % (i + 1), s4object(str(obj)))
                stderr.writeln(msg)
            if options.execute:
                try:
                    sql = obj.createddl(term=False)
                    cursor.execute(obj.dropddl(term=False))
                    cursor.execute(sql)
                except orasql.DatabaseError, exc:
                    if not options.ignore or 'ORA-01013' in str(exc):
                        raise
                    stderr.writeln('oradelete.py: ', s4error('%s: %s' % (exc.__class__, str(exc).strip())))

            else:
                sql = obj.dropddl(term=True) + obj.createddl(term=True)
                stdout.write(sql.encode(options.encoding))

    return


if __name__ == '__main__':
    sys.exit(main())